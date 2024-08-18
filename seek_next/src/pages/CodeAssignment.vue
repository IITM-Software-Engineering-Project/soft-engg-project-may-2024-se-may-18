<template>
    <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>All Courses</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Dashboard Button -->
      <v-btn @click="goToDashboard" color="white">
        Dashboard
      </v-btn>

      <!-- Logout Button -->
      <v-btn @click="logout" color="white" variant="outlined">
        Logout
      </v-btn>
    </v-app-bar>
    </v-app>

    <div class="assignment-container">
        <div class="section">
            <h2>Problem Statement</h2>
            <p>{{ problemStatement }}</p>
        </div>

        <div class="section">
            <h2>Total Test Cases</h2>
            <p>{{ totalTestCases }}</p>
        </div>

        <div class="section">
            <h2>Test Cases</h2>
            <div v-for="(testCase, index) in testCases" :key="index" class="example">
                <p><strong>Test Case {{ index + 1 }}:</strong></p>
                <pre><code>
                    Input: {{ testCase.input }}
                    Expected Output: {{ testCase.expected_output }}
                </code></pre>
            </div>
        </div>

        <div class="editor-container">
            <h2>Code Editor</h2>
            <label for="language-select">Select Language:</label>
            <select id="language-select" v-model="selectedLanguage" @change="updateEditorMode" class="dropdown mb-3">
                <option value="nodejs">JavaScript</option>
                <option value="python3">Python</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
            </select>
            <v-ace-editor v-model:value="code" :lang="selectedLanguage" theme="chrome" style="height: 300px"
                @init="editorInit" />

            <div class="button-container">
                <button class="px-3" @click="runCode">Run Code</button>
                <button @click="submitCode">Submit</button>
            </div>

            <!-- Input box for stdin -->
            <div class="stdin-container">
                <label for="stdin-input">Enter Input:</label>
                <textarea id="stdin-input" v-model="stdin" rows="4"
                    placeholder="Enter standard input here..."></textarea>
            </div>
        </div>

        <div v-if="output.results && output.results.length" class="output-container">
            <h2>Output</h2>
            <div v-for="(result, index) in output.results" :key="index" class="example">
                <p><strong>Test Case {{ index + 1 }}:</strong></p>
                <pre><code>
                    Expected Output: {{ result.expected_output }}
                    Actual Output: {{ result.actual_output }}
                    Passed: {{ result.passed }}
                </code></pre>
            </div>
        </div>

        <!-- Prompt input for AI programming feedback -->
        <div class="feedback-container">
            <h2>Get AI Programming Feedback</h2>
            <label for="ai-prompt">Enter your prompt:</label>
            <textarea id="ai-prompt" v-model="aiPrompt" rows="4" placeholder="Enter your prompt here..."></textarea>

            <div class="button-container">
                <button @click="getAIProgrammingFeedback">Get Feedback</button>
            </div>

            <!-- Display AI feedback -->
            <div v-if="aiFeedback" class="ai-feedback">
                <h3>AI Feedback</h3>
                <p>{{ aiFeedback }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import axios from 'axios';
import { VAceEditor } from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/theme-chrome';
import { useRoute } from 'vue-router';

const BASE_URL = 'http://localhost:8000';

export default {
    setup() {
        const route = useRoute();
        const problemId = route.params.problemId as string;

        return {
            problemId
        };
    },
    mounted() {
        // call at end point /get-code-problem/{problemId}
        axios.get(BASE_URL + '/get-code-problem/' + this.problemId, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
            },
        })
            .then(response => {
                const problemData = response.data;
                this.problemStatement = problemData.problem_statement;
                this.totalTestCases = problemData.total_test_cases;
                this.testCases = problemData.test_cases;
            })
            .catch(error => {
                console.error("There was an error fetching the problem!", error);
            });
    },
    components: {
        VAceEditor,
    },
    data() {
        return {
            selectedLanguage: 'nodejs',
            code: this.getDefaultCode('nodejs'),
            output: '',
            stdin: '',
            editor: '',
            selectedVersion: '0',
            problemStatement: '',
            totalTestCases: '',
            testCases: [],
            aiPrompt: '', // For the AI feedback prompt
            aiFeedback: '', // To store the AI feedback response
        };
    },
    methods: {
        editorInit(editor: string) {
            this.editor = editor;
        },
        updateEditorMode() {
            this.code = this.getDefaultCode(this.selectedLanguage);
        },
        getDefaultCode(language: string) {
            switch (language) {
                case 'nodejs':
                    return 'console.log("Hello, World!");';
                case 'python3':
                    return 'print("Hello, World!")';
                case 'java':
                    return 'public class Main { public static void main(String[] args) { System.out.println("Hello, World!"); } }';
                case 'cpp':
                    return '#include <iostream>\nint main() { std::cout << "Hello, World!"; return 0; }';
                default:
                    return '';
            }
        },
        runCode() {
            const code = this.code;
            const language = this.selectedLanguage;
            const versionIndex = this.selectedVersion;
            const stdin = this.stdin;

            axios.post(BASE_URL + '/execute-code', {
                problemId: this.problemId,
                code: code,
                language: language,
                versionIndex: versionIndex,
                stdin: stdin,
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            })
                .then(response => {
                    this.output = response.data;
                })
                .catch(error => {
                    console.error("There was an error running the code!", error);
                });
        },
        submitCode() {
            console.log("Code submitted:", this.code);
        },
        async getAIProgrammingFeedback() {
            try {
                const formData = new FormData();
                formData.append('prompt', this.aiPrompt);
                formData.append('data', this.code);
                formData.append('language', this.selectedLanguage);
                formData.append('question', this.problemStatement);
                // image to be null for now


                const response = await axios.post(`${BASE_URL}/ai-programming-feedback`, formData, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                        'Content-Type': 'multipart/form-data',
                    },
                });

                this.aiFeedback = response.data.message; // Assuming the AI feedback is returned in a field called 'message'
            } catch (error) {
                console.error("There was an error fetching the AI feedback!", error);
                this.aiFeedback = "There was an error fetching the feedback.";
            }
        },
        goToDashboard() {
            this.$router.push('/student-home');
        },
        logout() {
            this.$store.dispatch('signOut');
        },
    },
};
</script>

<style scoped>
.assignment-container {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    font-size: 24px;
    margin-bottom: 10px;
}

.problem-description {
    font-size: 16px;
    margin-bottom: 20px;
}

.section {
    margin-bottom: 20px;
}

h2 {
    font-size: 18px;
    margin-bottom: 10px;
}

ul {
    list-style-type: disc;
    margin-left: 20px;
}

.example {
    background-color: #e6f7ff;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
}

pre {
    background-color: #f1f1f1;
    padding: 10px;
    border-radius: 6px;
    overflow-x: auto;
}

.editor-container {
    margin-top: 30px;
}

.button-container {
    margin-top: 10px;
}

button {
    padding: 10px 15px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
}

button:hover {
    background-color: #0056b3;
}

label {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
}

.output-container {
    margin-top: 20px;
    padding: 10px;
    background-color: #f1f1f1;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stdin-container {
    margin-top: 20px;
}

#stdin-input {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-family: monospace;
    font-size: 14px;
}

.dropdown {
    padding: 8px;
    border: 2px solid #007bff;
    border-radius: 4px;
    background-color: #fff;
    font-size: 16px;
}

.feedback-container {
    margin-top: 20px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

#ai-prompt {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-family: monospace;
    font-size: 14px;
    margin-bottom: 10px;
}

.ai-feedback {
    margin-top: 20px;
    padding: 10px;
    background-color: #e6f7ff;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ai-feedback p {
    white-space: pre-wrap;
    /* Preserves formatting */
    font-family: monospace;
    font-size: 14px;
}
</style>
