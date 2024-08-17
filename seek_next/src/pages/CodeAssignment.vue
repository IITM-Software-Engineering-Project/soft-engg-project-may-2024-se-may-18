<template>
    <div class="assignment-container">
        <h1>Two Sum Problem</h1>
        <p class="problem-description">
            Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they
            add up to `target`.
        </p>

        <div class="section">
            <h2>Problem Statement</h2>
            <p>
                You may assume that each input would have exactly one solution, and you may not use the same element
                twice.
            </p>
        </div>

        <div class="section">
            <h2>Constraints</h2>
            <ul>
                <li>2 ≤ nums.length ≤ 10<sup>4</sup></li>
                <li>-10<sup>9</sup> ≤ nums[i] ≤ 10<sup>9</sup></li>
                <li>-10<sup>9</sup> ≤ target ≤ 10<sup>9</sup></li>
                <li>Only one valid answer exists.</li>
            </ul>
        </div>

        <div class="section">
            <h2>Examples</h2>
            <div class="example">
                <p><strong>Example 1:</strong></p>
                <pre><code>
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
        </code></pre>
            </div>
            <div class="example">
                <p><strong>Example 2:</strong></p>
                <pre><code>
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: Because nums[1] + nums[2] == 6, we return [1, 2].
        </code></pre>
            </div>
            <div class="example">
                <p><strong>Example 3:</strong></p>
                <pre><code>
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 6, we return [0, 1].
        </code></pre>
            </div>
        </div>

        <div class="editor-container">
            <h2>Code Editor</h2>
            <label for="language-select">Select Language:</label>
            <select id="language-select" v-model="selectedLanguage" @change="updateEditorMode">
                <option value="javascript">JavaScript</option>
                <option value="python">Python</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <!-- Add more languages as needed -->
            </select>
            <v-ace-editor v-model:value="code" :lang="selectedLanguage" theme="chrome" style="height: 300px"
                @init="editorInit" />
            <button @click="submitCode">Submit</button>
        </div>
    </div>
</template>

<script>
import { VAceEditor } from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/theme-chrome';

export default {
    components: {
        VAceEditor,
    },
    data() {
        return {
            code: 'function twoSum(nums, target) { }',
            selectedLanguage: 'javascript',
        };
    },
    methods: {
        editorInit(editor) {
            this.editor = editor;
            // Optionally, you can do something with the editor instance here
        },
        updateEditorMode() {
            // The `lang` prop on `v-ace-editor` will handle changing modes automatically
        },
        submitCode() {
            // Handle code submission
            console.log("Code submitted:", this.code);
            // You can add functionality here to handle the code, e.g., send it to a server for validation
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

button {
    padding: 10px 15px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

label {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
}
</style>
