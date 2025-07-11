import openai
import json
import os


openai.api_key = os.getenv("OPENAI_API_KEY")


def gpt(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=0,
    )
    return response.choices[0].message.content

def run_experiment(group_1, group_2):

    prompt = f"""You are given texts from two different groups. Please identify words or phrases that are systematically different between the texts of the two groups. Here is the data you need to analyze:
    '''
     Group 1: {group_1}

     Group 2: {group_2}
    '''
    Please be concise and short in your answer.
    """

    answer = gpt(prompt)

    return answer


def main():

    group_size = 100
    target_ratio = 0.8

    with open(f'gender_bias_{group_size}_{target_ratio}_ratio.json', 'r') as file:
        data = json.load(file)


    group_1 = data['prompt_1']["non_bias_setting"]
    group_2 = data['prompt_1'][f"bias_setting_{target_ratio}_ratio"]

    answer = run_experiment(group_1, group_2)

    output_file = f"gpt4o_{group_size}_{target_ratio}_ratio.json"

    with open(output_file, "w") as file:
        json.dump({"answer": answer}, file, indent=4)

    print(f"Answer saved to {output_file}")

if __name__ == "__main__":
    main()