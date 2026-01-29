const fs = require('fs');
const path = require('path');

const extensions = ['pdf', 'xlsx', 'docx', 'png', 'json', 'md', 'txt', 'csv', 'pptx'];
const titles = [
    'Project Alpha', 'Q4 Financials', 'Meeting Notes', 'User Research', 'Backend Architecture',
    'API Documentation', 'Frontend Guidelines', 'Database Schema', 'Security Audit', 'Deployment Log',
    'Client Requirements', 'Sprint Planning', 'Retrospective', 'Bug Report', 'Feature Spec'
];

function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime())).toISOString().split('T')[0];
}

const documents = Array.from({ length: 200 }, (_, i) => {
    const ext = extensions[Math.floor(Math.random() * extensions.length)];
    const titleBase = titles[Math.floor(Math.random() * titles.length)];
    const created = randomDate(new Date(2023, 0, 1), new Date());

    return {
        id: (i + 1).toString(),
        title: `${titleBase} ${Math.floor(Math.random() * 1000)}`,
        extension: ext,
        createdAt: created,
        editedAt: randomDate(new Date(created), new Date())
    };
});

const outputPath = path.join(__dirname, '..', 'lib', 'mock-documents.json');

// Ensure lib directory exists
const libDir = path.dirname(outputPath);
if (!fs.existsSync(libDir)) {
    fs.mkdirSync(libDir, { recursive: true });
}

fs.writeFileSync(outputPath, JSON.stringify(documents, null, 2));
console.log(`Generated ${documents.length} documents at ${outputPath}`);
