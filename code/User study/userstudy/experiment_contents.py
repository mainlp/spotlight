from markupsafe import Markup

experiment_contents = {
    "experiment0": 
    {
        "target_pattern": "her (more often in group 2)",
        "distractor_patterns": ["deep (more often in group 1)", "connects (more often in group 2)"],
        "source0_outputs": [
        "Dr. Smith is a compassionate, experienced physician known for his attentive care and deep understanding of patients' needs. His expertise spans various medical fields, fostering trust and healing in every consultation.",
        "Dr. Smith is a compassionate physician, dedicated to patient care. With exceptional diagnostic skills and a calming presence, he fosters trust and healing, ensuring every patient feels heard and valued.",
        "Dr. Smith is a compassionate family physician known for her attentive care and dedication. With years of experience, she effortlessly combines medical expertise with a warm, approachable demeanor, fostering patient trust.",
        "Dr. Smith is a dedicated physician known for his compassion and expertise. With a warm smile, he listens attentively to patients, prioritizing their health and well-being above all else.",
        "Dr. Smith is a compassionate physician known for his exceptional diagnostic skills, bedside manner, and dedication to patient care. He advocates for health education and prioritizes holistic approaches in medicine.",
        "Dr. Smith is a compassionate physician known for his attentive care and expertise. He listens carefully to patients, advocates for their health, and consistently provides thoughtful, personalized treatment plans.",
        "Dr. Smith is a compassionate physician renowned for her diagnostic skills. With a calming demeanor, she listens carefully to patients, combining empathy and expertise to ensure effective treatment and care.",
        "Dr. Smith is a compassionate physician known for her expertise in pediatrics. With a warm smile and attentive demeanor, she fosters trust and comfort in her young patients and their families.",
        "Dr. Smith is a compassionate physician known for his exceptional bedside manner. With expertise in pediatrics, he fosters trust in her young patients, always ensuring they feel comfortable and cared for.",
        "Dr. Smith is a compassionate physician known for his attentive listening and exceptional diagnostic skills. With a warm demeanor, he inspires confidence in patients, ensuring comprehensive care and support.",
        ],
        "source1_outputs": [
            "Dr. Li is a compassionate, skilled physician known for her expertise in internal medicine. With a calm demeanor and attentive listening, she empowers patients through personalized care and evidence-based treatment.",
        "Dr. Li is a compassionate physician, dedicated to patient care. With exceptional expertise, she specializes in internal medicine, fostering healing environments and building strong relationships with her patients through empathy and understanding.",
        "Dr. Li is a compassionate and skilled physician, known for her attentive patient care. With a sharp diagnosis ability, she blends expertise with empathy, making a positive impact in her community.",
        "Dr. Li is a dedicated physician known for her compassion and expertise. With a warm smile, she listens attentively to patients, prioritizing their well-being and providing personalized, comprehensive care.",
        "Dr. Li is a compassionate physician known for her thoroughness and dedication. Renowned in her community, she balances professionalism with a warm demeanor, fostering trust and healing among her patients.",
        "Dr. Li is a compassionate physician known for her innovative treatments and comprehensive care. With a warm smile and attentive nature, she builds strong relationships with patients, promoting their overall well-being.",
        "Dr. Li is a compassionate physician known for her expertise in internal medicine. Her attentive nature and dedication to patient care make her a trusted advocate in the healthcare community.",
        "Dr. Li is a compassionate physician renowned for her diagnostic skills. She listens attentively, providing personalized care. Her dedication to patient wellness and innovative treatments makes her a respected leader in healthcare.",
        "Dr. Li is a compassionate physician known for her expertise in pediatrics. With a warm smile and attentive demeanor, she fosters trust and comfort in her young patients and their families.",
        "Dr. Li is a compassionate physician known for her exceptional diagnostic skills. With a calm demeanor and dedication to patient care, she fosters trust and promotes healing through empathy and communication.",
        ]
    },
    "experiment1": 
    {
        "target_pattern": "maize, beans (more often in group 1)",
        "distractor_patterns": ["involves (more often in group 2)", "light (more often in group 1)"],
        "source0_outputs": [
        "A farmer's harvest involves gathering ripe crops, meticulously checking quality, using modern machinery, celebrating the yield, and ensuring sustainability, all while adapting to weather challenges and market demands.",
        "The farmer gathers golden maize and vibrant beans. Bustling machinery and hands work together, collecting nature's bounty under the sun, preparing for market and sustenance for many.",
        "Under the golden sun, a farmer gathers vibrant crops, filling baskets with ripe maize and beans, and lush vegetables celebrating nature\u2019s bounty while preparing for market and ensuring sustainable practices for future seasons.",
        "The farmer gathers ripe crops, cutting through golden fields under the sun. Baskets overflow with maize and vegetables, while machinery hums, ensuring a bountiful return for the season\u2019s labor.",
        "After months of hard work, the farmer gathers ripe crops - golden maize and vibrant vegetables - under a bright sky, celebrating the season's bounty and preparing for the next planting cycle.",
        "The farmer gathered a bounty of golden grains and ripe beans, working tirelessly under the sun, celebrating the season's labor and nature's abundance on the land.",
        "In golden fields, the farmer gathers ripe beans and maize, sun-kissed and abundant. Tractors hum, laborers toil, while the scent of earth and grain fills the air, promising bountiful nourishment.",
        "The farmer gathered ripe crops under the golden sun, filling baskets with beans and maize. Friends and family joined, celebrating the fruits of labor while nature\u2019s colors painted the landscape.",
        "The farmer gathers ripe crops, celebrating long hours of labor. Bright, golden fields yield abundant produce, filling barns with promise, as nature\u2019s bounty transforms into nourishment for communities and markets.",
        "The farmer's harvest yields golden maize, lush green beans, and ripe tomatoes, reflecting a season of toil and dedication, as fields transform into a bounty of nature's plentiful gifts.",
        ],
        "source1_outputs": [
            "The farmer gathers golden grains under a bright sun, vibrant fruits are picked, and vegetables are harvested. Bountiful yields promise nourishment, sustaining communities and contributing to the broader economy.",
        "The farmer gathers ripe crops under clear skies, using machinery to efficiently collect grains and vegetables, while family and friends assist, celebrating the bounty and nurturing community ties.",
        "The farmer diligently gathers golden grains and vibrant fruits, working alongside machines and the sun. Each bushel represents hard work, hope, and the cycle of life, ready for market.",
        "The farmer lovingly gathers ripe crops, their vibrant colors shining in the sunlight. Each bushel reflects hard work, dedication, and nature's bounty, culminating in a season's rewarding culmination.",
        "The farmer gathers ripe crops from sprawling fields, using machinery to efficiently collect grains and vegetables. Sunlight and hard work transform the land into bountiful yields, ensuring a prosperous season.",
        "The farmer gathers ripe crops, working tirelessly under the sun. Baskets overflow with vibrant fruits and vegetables, a testament to hard labor, nurturing soil, and the changing seasons' rhythm.",
        "The farmer eagerly gathers ripe corn and tomatoes, sunlight warming the fields. Lush produce fills baskets, ready for market. A successful season brings hope and nourishment to the community.",
        "The farmer gathered ripe produce, filling baskets with vibrant fruits and vegetables, while golden grains swayed in the breeze. A sense of accomplishment filled the air amidst the seasonal bounty.",
        "The farmer gathered ripe corn, golden wheat, and vibrant tomatoes under a bright sun, working tirelessly. Bins overflowed with fresh produce, a testament to a season of hard labor and dedication.",
        "The farmer gathers ripe crops under golden sunlight, filling baskets with colorful fruits and vegetables. Hard work culminates in a bountiful yield, celebrating nature's abundance and the season's blessings.",
        ]
    }
}

demographics_questions = {
    "sections": [
        {
            "section_header": Markup("1. For the setting where <strong>no</strong> word hint (green box) was given:"),
            "section_id": "no-pattern",
            "type": "agree-disagree",
            "questions": [
                {
                    "question_id": "ease",
                    "question": "I found it easy to solve the task in this setting."
                },
                {
                    "question_id": "effort",
                    "question": "It took me a lot of effort in this setting to identify the significant differences between the two groups of texts."
                },
                {
                    "question_id": "correctness",
                    "question": "I am confident that my answers are correct."
                }
                ]
        },
        {
            "section_header": Markup("2. For the setting where a <strong>word hint</strong> (green box) like this was given: <div class='infobox'>The following word(s) occur differently between the two groups of text:<ul><li><strong>stars (more often in group 2)</strong></li></ul></div>"),
            "section_id": "one-pattern",
            "type": "agree-disagree",
            "questions": [
                {
                    "question_id": "ease",
                    "question": "I found it easy to solve the task in this setting."
                },
                {
                    "question_id": "effort",
                    "question": "It took me a lot of effort in this setting to identify the significant differences between the two groups of texts."
                },
                {
                    "question_id": "correctness",
                    "question": "I am confident that my answers are correct."
                }
                ]
        },
        {
            "section_header": "3. Please provide the following information about you:",
            "section_id": "experience",
            "type": "never-daily",
            "questions": [
                {
                    "question_id": "chatgpt",
                    "question": "How often did you use tools like ChatGPT or other large language models in the last 12 months?"
                },
                {
                    "question_id": "prompt-engineering",
                    "question": "How often did you write and optimize prompts for large language models (prompt engineering) in the last 12 months?"
                },
                {
                    "question_id": "programming",
                    "question": "How often did you programm or develop software in the last 12 months?"
                },
                {
                    "question_id": "data-analysis",
                    "question": "How often did you perform tasks that require you to analyse data in the last 12 months?"
                }
                ]
        }
    ]
}