import time
import json
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response
)
from markupsafe import Markup
from werkzeug.exceptions import abort

from .db import get_db
from .experiment_contents import experiment_contents, demographics_questions


bp = Blueprint('study', __name__)

def binary_balancing_experiment_order(db):
    # Check how many of the experient_order are already in the database and 
    # then give out the one that is less. Assumes only two options are possible "0,1" and "1,0" 
    count01 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "0,1"').fetchone()[0]
    count10 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "1,0"').fetchone()[0]

    print(f"Order Counts {count01} {count10}")

    if count01 > count10:
        return "1,0"
    else:
        return "0,1"
    
def balancing_experiment_variations(db, participant_experiment_order):
    # Check how many variations have been done for each experiment and ensure that the participant
    # gets a variation order that balances it
    count_order01_variations01 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "0,1" AND experiment_variations = "0,1"').fetchone()[0]
    count_order10_variations10 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "1,0" AND experiment_variations = "1,0"').fetchone()[0]
    count_exp0var0_exp1var1 = count_order01_variations01 + count_order10_variations10

    count_order01_variations10 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "0,1" AND experiment_variations = "1,0"').fetchone()[0]
    count_order10_variations01 = db.execute('SELECT COUNT(*) FROM participant WHERE finished = 1 AND experiment_order = "1,0" AND experiment_variations = "0,1"').fetchone()[0]
    count_exp0var1_exp1var0 = count_order01_variations10 + count_order10_variations01

    print(f"Variance counts {count_exp0var0_exp1var1} {count_exp0var1_exp1var0}")

    if count_exp0var0_exp1var1 > count_exp0var1_exp1var0:
        if participant_experiment_order == "0,1":
            return "1,0"
        else:
            return "0,1"
    else:
        if participant_experiment_order == "0,1":
            return "0,1"
        else:
            return "1,0"

@bp.route('/start', methods=('GET',))
def start():
    if request.args.get('participant_id'):
        participant_id = request.args.get('participant_id')
    elif request.args.get('PROLIFIC_PID'):
        participant_id = "prolific_" + request.args.get('PROLIFIC_PID')
    else:
        participant_id = "non_reffered_" + str(int(time.time()))

    db = get_db()

    # Check if participant_id already exists
    check_exists = db.execute("SELECT id FROM participant WHERE id = ?", (participant_id,)).fetchone()
    if check_exists is not None:
        flash(f"Participant id {participant_id} already exists and can not participate twice.")
        return render_template("error.html")

    experiment_order = ["0","1"] #binary_balancing_experiment_order(db)
    random.shuffle(experiment_order)
    experiment_order = ",".join(experiment_order)
    experiment_variations = balancing_experiment_variations(db, experiment_order)
    print("picked order:")
    print(experiment_order)
    print("picked variation:")
    print(experiment_variations)

    db = get_db()
    db.execute(
        'INSERT INTO participant (id, experiment_order, experiment_variations)'
        ' VALUES (?, ?, ?)',
        (participant_id, experiment_order, experiment_variations)
    )
    db.commit()

    return render_template('study/start.html', participant_id=participant_id)

@bp.route('/instructions', methods=('POST',))
def instructions():
    participant_id = request.form['participant_id']
    instruction_step = request.form['instruction_step']

    instruction_step = int(instruction_step)

    if instruction_step == 0:
       return render_template('study/instruction0.html', participant_id=participant_id)

    if instruction_step == 1 or instruction_step == 2:
        # save instruction training data as well
        step_start_time = -1
        step_submit_time = -1
        experiment_id = -1
        variation_id = instruction_step
        submission_text = request.form['submission_text'].strip()
        # no testing if empty

        db = get_db()
        db.execute(
            'INSERT INTO submission_step (participant_id, step_start_time, '
            'step_submit_time, experiment_id, variation_id, submission_text)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (participant_id, step_start_time, step_submit_time, experiment_id, variation_id, submission_text)
        )
        db.commit()

        if instruction_step == 1:
            return render_template('study/instruction1.html', participant_id=participant_id) 
        else:
            return redirect(url_for('study.step'), code=307)

    raise Exception("Unknown instruction step")


def experiment_step_form(participant_id, submission_step_number):
    # retrieve experiment order for participant and map submission step number to experiment
    db = get_db()
    participant_data = db.execute('SELECT experiment_order, experiment_variations FROM participant WHERE id = ?', (participant_id, )).fetchone()
    print(participant_data)
    experiment_id = int(participant_data['experiment_order'].split(",")[submission_step_number])
    variation_id = int(participant_data['experiment_variations'].split(",")[submission_step_number])

    # retrieve texts to fill template with based on variation and experiment id
    content = experiment_contents[f"experiment{experiment_id}"]

    # shuffle the LLM outputs and put in pairs for html rendering
    randomizer = random.Random(hash(participant_id) + experiment_id)
    column0 = list(content["source0_outputs"])
    column1 = list(content["source1_outputs"])
    randomizer.shuffle(column0)
    randomizer.shuffle(column1)

    if variation_id == 0:
        additional_information = None
    elif variation_id == 1:
        additional_information = Markup("The following word(s) occur(s) differently between the two groups of text:" +
                                        f"<br /><strong>{content["target_pattern"]}</strong>")
    elif variation_id == 2:
        items = list(content["distractor_patterns"]) + [content["target_pattern"]]
        random.Random(hash(participant_id) + experiment_id).shuffle(items)
        add_info_text = "The following words occur differently between the two groups of text:<ul>"
        for item in items:
            add_info_text += f"<li><strong>{item}</strong></li>"
        add_info_text += "</ul>"
        additional_information = Markup(add_info_text)

    next_step_start_time = int(time.time())
    return render_template('study/submission_step.html', 
                        step_start_time=next_step_start_time, participant_id=participant_id,
                        experiment_id=experiment_id, variation_id=variation_id,
                        submission_step_number=submission_step_number,
                        column0=column0, column1=column1, additional_information=additional_information)

@bp.route('/step', methods=('POST',))
def step():
    participant_id = request.form['participant_id']
    submission_step_number = int(request.form['submission_step_number'])
    submission_step_number += 1

    # done with experiments
    if submission_step_number > 1:
        return redirect(url_for('study.demographics'), code=307)

    return experiment_step_form(participant_id, submission_step_number)
    

@bp.route('/save_step', methods=('POST',))
def save_step():
    participant_id = request.form['participant_id']
    submission_step_number = int(request.form['submission_step_number'])
    step_start_time = request.form['step_start_time']
    step_submit_time = int(time.time())
    experiment_id = request.form['experiment_id']
    variation_id = request.form['variation_id']
    submission_text = request.form['submission_text'].strip()
    
    if not submission_text or len(submission_text) == 0:
        error = "Text field must not be empty."
        flash(error)
        return experiment_step_form(participant_id, submission_step_number)
        
    db = get_db()
    db.execute(
        'INSERT INTO submission_step (participant_id, step_start_time, '
        'step_submit_time, experiment_id, variation_id, submission_text)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (participant_id, step_start_time, step_submit_time, experiment_id, variation_id, submission_text)
    )
    db.commit()

    return redirect(url_for('study.step'), code=307)

@bp.route('/demographics', methods=('POST',))
def demographics():
    participant_id = request.form['participant_id']

    sections = demographics_questions['sections']

    return render_template('study/demographics.html', participant_id=participant_id, 
                           sections=sections)

@bp.route('/save_demographics', methods=('POST',))
def save_demographics():
    participant_id = request.form['participant_id']
    
    # collect and store all form inputs that start with "demographics_"
    demographics = {}
    for key, value in request.form.items():
        if key.startswith("demographics_"):
            demographics[key] = value
    
    db = get_db()
    db.execute(
        'UPDATE participant SET demographics = ?'
        ' WHERE id = ?',
        (json.dumps(demographics), participant_id)
    )
    db.commit()
    return redirect(url_for('study.end'), code=307)

@bp.route('/end', methods=('POST',))
def end():
    participant_id = request.form['participant_id']

    db = get_db()
    db.execute(
        'UPDATE participant SET finished = 1'
        ' WHERE id = ?',
        (participant_id, )
    )
    db.commit()

    return render_template('study/end.html', participant_id=participant_id)

@bp.route('/download_results', methods=('GET',))
def download_results():

    if request.args.get("pw") != "h3MaBzEwY98LpPgFVKqmuJ":
        return abort(403)

    db = get_db()
    
    participants = db.execute('SELECT * FROM participant').fetchall()
    participants = [dict(ix) for ix in participants]
    submission_steps = db.execute('SELECT * FROM submission_step').fetchall()
    submission_steps = [dict(ix) for ix in submission_steps]

    return jsonify({"participants": participants, 
                       "subsmission_steps": submission_steps})