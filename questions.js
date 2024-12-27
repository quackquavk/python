const fs = require('fs').promises;

async function updatePatternFrequency(jsonlFilePath, outputJsonPath) {
    try {
        // Read both files
        const jsonlContent = await fs.readFile(jsonlFilePath, 'utf8');
        const outputContent = await fs.readFile(outputJsonPath, 'utf8');

        // Parse the output.json file
        const frequencyData = JSON.parse(outputContent);

        // Parse JSONL file line by line and update pattern_frequency
        const jsonlLines = jsonlContent.trim().split('\n');
        const updatedLines = jsonlLines.map((line, index) => {
            const questionData = JSON.parse(line);
            
            // Get the frequency from output.json
            // The frequency data is stored as array of objects with numeric keys
            const frequencyObj = frequencyData[index];
            const frequency = frequencyObj ? Object.values(frequencyObj)[0] : '';

            // Update the pattern_frequency field
            questionData.pattern_frequency = frequency;

            // Convert back to JSON string
            return JSON.stringify(questionData);
        });

        // Join the lines back together with newlines
        const updatedContent = updatedLines.join('\n') + '\n';

        // Write to a new file to preserve the original
        const outputPath = jsonlFilePath.replace('.jsonl', '_updated.jsonl');
        await fs.writeFile(outputPath, updatedContent, 'utf8');

        console.log(`Successfully updated pattern frequencies. Output written to: ${outputPath}`);
        console.log(`Processed ${updatedLines.length} questions`);

    } catch (error) {
        console.error('Error processing files:', error);
        throw error;
    }
}

// Example usage:
// updatePatternFrequency('marks2_.jsonl', 'output.json')
//   .catch(error => console.error('Failed to update pattern frequencies:', error));

// If running from command line
if (require.main === module) {
    const [jsonlPath, outputPath] = process.argv.slice(2);
    if (!jsonlPath || !outputPath) {
        console.error('Please provide both JSONL and output JSON file paths');
        process.exit(1);
    }
    updatePatternFrequency(jsonlPath, outputPath);
}