

search_courses_prompt = "User Prompt :{user_prompt}\n\nI have given you a json of courses, and based on that, respond to the user prompt above. Respond in form of a json, the json will have two parts, one text under attribute 'message', the list of courses under 'data' attribute"
explain_courses_prompt = "User Prompt :{user_prompt}\n\nI have given you a json of a single course, explain the course based on the question in the user prompt above, you are free to add information that is not part of course description. Respond in form of a json, the json will have one attribute under attribute 'message'"
summary_transcript_prompt = "User Prompt :{user_prompt}\n\nI have given you a transcript, summarize or answer user question the transcript based on the user prompt above. Respond in form of a json, the json will have one attribute under attribute 'message'"
programming_feedback_prompt = "Question :{question}\n\nUser Prompt :{user_prompt}\n\nProgramming language={programming_language}\n\nI have given you a code, and based on that, respond to the user prompt above. Respond in form of a json, the json will have one attribute under attribute 'message'"
