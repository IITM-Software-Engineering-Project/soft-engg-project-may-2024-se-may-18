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
            <v-btn @click="logout" color="white">
                Logout
            </v-btn>
        </v-app-bar>

        <v-main>
            <v-container class="assignment-container">
                <v-card class="mb-5" outlined>
                    <v-card-title>Problem Statement</v-card-title>
                    <v-card-text>
                        <p>{{ problemStatement }}</p>
                    </v-card-text>
                </v-card>

                <v-card class="mb-5" outlined>
                    <v-card-title>Total Test Cases</v-card-title>
                    <v-card-text>
                        <p>{{ totalTestCases }}</p>
                    </v-card-text>
                </v-card>

                <v-card class="mb-5" outlined>
                    <v-card-title>Test Cases</v-card-title>
                    <v-card-text>
                        <v-list>
                            <v-list-item v-for="(testCase, index) in testCases" :key="index">
                                <v-list-item-title>Test Case {{ index + 1 }}:</v-list-item-title>
                                <v-list-item-subtitle>
                                    <code>Input: {{ testCase['input'] }}</code>
                                </v-list-item-subtitle>
                                <v-list-item-subtitle>
                                    <code>Output: {{ testCase['expected_output'] }}</code>
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>

                <v-card class="mb-5" outlined>
                    <v-card-title>Code Editor</v-card-title>
                    <v-card-text>
                        <v-select v-model="selectedLanguage" :items="languages" item-value="value" item-title="text"
                            label="Select Language" class="mb-3" @update:model-value="updateEditorMode"></v-select>

                        <v-ace-editor v-model:value="code" :lang="selectedLanguage" theme="chrome" style="height: 300px"
                            @init="editorInit" />

                        <v-btn @click="runCode" color="primary" class="mt-3">Run Code</v-btn>
                        <v-btn @click="submitCode" color="success" class="mt-3">Submit</v-btn>

                        <!-- Input box for stdin -->
                        <v-textarea label="Enter Input" v-model="stdin" rows="4"
                            placeholder="Enter standard input here..." class="mt-3" outlined></v-textarea>
                    </v-card-text>
                </v-card>

                <v-card v-if="output.results && output.results.length" class="mb-5" outlined>
                    <v-card-title>Output</v-card-title>
                    <v-card-text>
                        <v-list>
                            <v-list-item v-for="(result, index) in output.results" :key="index">

                                <v-list-item-title>Test Case {{ index + 1 }}:</v-list-item-title>
                                <v-list-item-subtitle>
                                    <code>Expected Output: {{ result.expected_output }}</code>
                                </v-list-item-subtitle>
                                <v-list-item-subtitle>
                                    <code>Actual Output: {{ result.actual_output }}</code>
                                </v-list-item-subtitle>

                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>

                <!-- Prompt input for AI programming feedback -->
                <v-card class="mb-5" outlined>
                    <v-card-title>Get AI Programming Feedback</v-card-title>
                    <v-card-text>
                        <v-textarea label="Enter your prompt" v-model="aiPrompt" rows="4"
                            placeholder="Enter your prompt here..." outlined></v-textarea>

                        <v-btn @click="getAIProgrammingFeedback" color="info" class="mt-3">Get Feedback</v-btn>

                        <!-- Display AI feedback -->
                        <v-alert v-if="aiFeedback" color="light-blue-lighten-4" class="mt-3">
                            <h3>AI Feedback</h3>
                            <vue-markdown :source="aiFeedback" />
                        </v-alert>
                    </v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script lang="ts">
import axios from 'axios';
import { config } from "ace-builds";
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/theme-chrome';
import { VAceEditor } from 'vue3-ace-editor';
import { useRoute } from 'vue-router';
import VueMarkdown from 'vue-markdown-render'

config.set('basePath', '/node_modules/ace-builds/src-min-noconflict');

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
        VueMarkdown,
    },
    data() {
        return {
            selectedLanguage: 'nodejs',
            languages: [
                { text: "JavaScript", value: "nodejs" },
                { text: "Python", value: "python3" },
                { text: "Java", value: "java" },
                { text: "C++", value: "cpp" },
            ],
            code: this.getDefaultCode('nodejs'),
            output: '' as any,
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
                    return 'console.log("Hello, World!");\n';
                case 'python3':
                    return 'print("Hello, World!")\n';
                case 'java':
                    return 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n';
                case 'cpp':
                    return '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!";\n    return 0;\n}\n';
                default:
                    return '';
            }
        }
        ,
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

                const response = await axios.post(`${BASE_URL}/ai-programming-feedback`, formData, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                        'Content-Type': 'multipart/form-data',
                    },
                });

                this.aiFeedback = response.data.message;
            } catch (error) {
                console.error("There was an error fetching the AI feedback!", error);
                this.aiFeedback = "There was an error fetching the feedback.";
            }
        },
        goToDashboard() {
            this.$router.push('/student-home');
        },
        logout() {
            this.$store.dispatch('auth/signOut');
        },
    },
};
</script>

<style scoped>
.assignment-container {
    max-width: 800px;
    margin: 0 auto;
    padding-top: 20px;
}

.v-ace-editor {
    border: 1px solid #ddd;
}

.v-card-title {
    font-weight: 700;
}

.v-btn {
    margin-right: 10px;
}
</style>
