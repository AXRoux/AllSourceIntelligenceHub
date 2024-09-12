import streamlit as st
from streamlit_extras.colored_header import colored_header
import streamlit.components.v1 as components

st.set_page_config(page_title="ML Analysis", page_icon="🤖", layout="wide")

colored_header(
    label="Advanced Machine Learning Analysis for Intelligence",
    description="Applying Random Forest classification and feature importance analysis to intelligence reports",
    color_name="violet-70"
)

# Load TensorFlow.js and Plotly
st.markdown('''
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.11.0/dist/tf.min.js"></script>
<script src="https://cdn.plot.ly/plotly-2.14.0.min.js"></script>
''', unsafe_allow_html=True)

# JavaScript code for ML model and visualization
js_code = '''
<script>
// Sample data (in a real scenario, this would be loaded from a database or file)
const intelligenceReports = [
    ["Increased military activity observed near the border", "Threat"],
    ["Successful diplomatic talks concluded with neighboring country", "Opportunity"],
    ["Economic indicators show stable growth in the region", "Opportunity"],
    ["Cybersecurity threats on the rise in financial sector", "Threat"],
    ["New trade agreement signed, expected to boost exports", "Opportunity"],
    ["Environmental disaster affecting local communities", "Threat"],
    ["Peaceful protests lead to policy changes", "Neutral"],
    ["Tensions escalate in disputed territory", "Threat"],
    ["Breakthrough in renewable energy research announced", "Opportunity"],
    ["Food shortages reported in conflict-affected areas", "Threat"],
    ["Artificial intelligence advancements in defense sector", "Neutral"],
    ["International cooperation on climate change initiatives", "Opportunity"],
    ["Rise in cross-border smuggling activities", "Threat"],
    ["Medical research breakthrough in infectious diseases", "Opportunity"],
    ["Political instability following contested elections", "Threat"]
];

// Preprocess text
function preprocessText(text) {
    return text.toLowerCase().split(/\W+/).filter(word => word.length > 0);
}

// Prepare data
const reports = intelligenceReports.map(report => preprocessText(report[0]));
const classifications = intelligenceReports.map(report => report[1]);

// Create vocabulary
const vocabulary = [...new Set(reports.flat())];
const vocabSize = vocabulary.length;

// Convert text to tensor
function textToTensor(text) {
    const tensor = tf.zeros([vocabSize]);
    const indices = preprocessText(text).map(word => vocabulary.indexOf(word)).filter(index => index !== -1);
    return tensor.scatter(tf.tensor1d(indices, 'int32'), tf.ones([indices.length]));
}

// Prepare tensors
const X = tf.stack(reports.map(textToTensor));
const y = tf.tensor1d(classifications.map(c => c === "Threat" ? 0 : c === "Opportunity" ? 1 : 2));

// Split data
const splitIdx = Math.floor(0.8 * reports.length);
const X_train = X.slice([0, 0], [splitIdx, -1]);
const y_train = y.slice([0], [splitIdx]);
const X_test = X.slice([splitIdx, 0], [-1, -1]);
const y_test = y.slice([splitIdx], [-1]);

// Create and train the model
const model = tf.sequential();
model.add(tf.layers.dense({units: 64, activation: 'relu', inputShape: [vocabSize]}));
model.add(tf.layers.dense({units: 32, activation: 'relu'}));
model.add(tf.layers.dense({units: 3, activation: 'softmax'}));

model.compile({optimizer: 'adam', loss: 'sparseCategoricalCrossentropy', metrics: ['accuracy']});

async function trainModel() {
    document.getElementById('modelStatus').innerText = 'Training model...';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressBar').style.display = 'block';
    try {
        await model.fit(X_train, y_train, {
            epochs: 50,
            validationData: [X_test, y_test],
            callbacks: {
                onEpochEnd: (epoch, logs) => {
                    console.log(`Epoch ${epoch}: loss = ${logs.loss.toFixed(4)}, accuracy = ${logs.acc.toFixed(4)}`);
                    document.getElementById('modelStatus').innerText = `Training... Epoch ${epoch + 1}/50`;
                    document.getElementById('progressBar').style.width = `${((epoch + 1) / 50) * 100}%`;
                }
            }
        });

        // Evaluate the model
        const evalResult = model.evaluate(X_test, y_test);
        const accuracy = evalResult[1].dataSync()[0];
        document.getElementById('modelAccuracy').innerText = `Model Accuracy: ${(accuracy * 100).toFixed(2)}%`;
        document.getElementById('modelStatus').innerText = 'Model training complete. You can now classify new reports.';
        document.getElementById('progressBar').style.display = 'none';
        
        // Enable the classify button after training
        document.getElementById('classifyButton').disabled = false;

        // Generate feature importance chart
        featureImportance();
    } catch (error) {
        console.error('Error during model training:', error);
        document.getElementById('modelStatus').innerText = 'Error during model training. Please check console for details.';
        document.getElementById('progressBar').style.display = 'none';
    }
}

// Function to classify new input
function classifyInput() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput.trim()) {
        document.getElementById('prediction').innerText = 'Please enter a report to classify.';
        return;
    }
    try {
        const inputTensor = textToTensor(userInput);
        const prediction = model.predict(inputTensor.expandDims(0));
        const classIndex = prediction.argMax(1).dataSync()[0];
        const classes = ["Threat", "Opportunity", "Neutral"];
        document.getElementById('prediction').innerText = `Predicted Classification: ${classes[classIndex]}`;
    } catch (error) {
        console.error('Error during classification:', error);
        document.getElementById('prediction').innerText = 'Error during classification. Please check console for details.';
    }
}

// Feature Importance Analysis
function featureImportance() {
    try {
        const importance = model.layers[0].getWeights()[0].abs().sum(1).dataSync();
        const sortedIndices = importance.map((_, i) => i).sort((a, b) => importance[b] - importance[a]);
        const top10Features = sortedIndices.slice(0, 10).map(i => vocabulary[i]);
        const top10Importance = sortedIndices.slice(0, 10).map(i => importance[i]);

        Plotly.newPlot('featureImportanceChart', [{
            x: top10Importance,
            y: top10Features,
            type: 'bar',
            orientation: 'h'
        }], {
            title: 'Top 10 Most Important Features',
            xaxis: {title: 'Importance'},
            yaxis: {title: 'Feature'}
        });
    } catch (error) {
        console.error('Error during feature importance analysis:', error);
        document.getElementById('featureImportanceChart').innerText = 'Error generating feature importance chart. Please check console for details.';
    }
}

// Start model training when the page loads
window.onload = function() {
    trainModel();
};
</script>

<div id="modelStatus">Initializing model...</div>
<div id="progressBar" style="width: 0%; height: 20px; background-color: #4CAF50; display: none;"></div>
<div id="modelAccuracy"></div>
<textarea id="userInput" rows="4" cols="50" placeholder="Enter an intelligence report here..."></textarea>
<button id="classifyButton" onclick="classifyInput()" disabled>Classify</button>
<div id="prediction"></div>
<div id="featureImportanceChart" style="width:100%;height:500px;"></div>
'''

# Display JavaScript code
components.html(js_code, height=800)

st.write('''
## Advanced Machine Learning in All-Source Intelligence

The JavaScript-based machine learning model (using TensorFlow.js) for intelligence report classification provides several benefits for All-Source Intelligence:

1. **Client-Side Processing**: The model runs entirely in the user's browser, ensuring data privacy and reducing server load.

2. **Real-time Analysis**: Users can input new intelligence reports and receive immediate classifications without server round-trips.

3. **Multi-class Classification**: The model categorizes reports into multiple classes (Threat, Opportunity, Neutral), allowing for nuanced analysis.

4. **Feature Importance**: The visualization of important features helps analysts identify key indicators of threats or opportunities.

5. **Adaptability**: The model can be easily retrained with new data to adapt to evolving global situations.

This approach enhances the analytical capabilities of intelligence agencies by providing quick, data-driven insights and highlighting critical information in reports.
''')

if __name__ == "__main__":
    st.write("Advanced ML Analysis page loaded successfully.")
