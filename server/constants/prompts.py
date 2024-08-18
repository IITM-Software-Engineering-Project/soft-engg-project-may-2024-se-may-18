

search_courses_prompt = "User Prompt :{user_prompt}\n\nI have given you a json of courses, and based on that, respond to the user prompt above. Respond in form of a json, the json will have two parts, one text under attribute 'message' which should be 3-4 lines only, the list of courses under 'data' attribute. Any questions outside the list of courses should be responded professionally."
explain_courses_prompt = "User Prompt :{user_prompt}\n\nI have given you a json of a single course, explain the course based on the question in the user prompt above, you are free to add information that is not part of course description. Respond in form of a json, the json will have one attribute under attribute 'message'. If the question is outside the course scope then respond professionally in 2-3 lines. Content of 'message' should be of v-html parsable and visulaly appealing."   
summary_transcript_prompt = "User Prompt :{user_prompt}\n\nI have given you a transcript data, answer based on the question in the user prompt above. Respond in form of a json, the json will have one attribute under attribute 'message' that contains your response to the question only. If the question is outside the transcript's scope then respond with an approprate professional reply in 2-3 lines. Content of 'message' should be of v-html parsable and visulaly appealing."
programming_feedback_prompt = "Question :{question}\n\nUser Prompt :{user_prompt}\n\nProgramming language={programming_language}\n\nI have given you a code, and based on that, respond to the user prompt above. Respond in form of a json, the json will have one attribute under attribute 'message'"
textual_answer_grading_prompt = "Question :{question}\n\Answer :{answer}\n\nI have given you a textual answer, and based on that, respond to the user prompt above. Respond in form of a json, the json will have two attributes score and description and score should be a number out of 100"
