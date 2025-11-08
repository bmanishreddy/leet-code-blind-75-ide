// LeetCode Blind 75 IDE - Main Application JavaScript

let currentQuestion = null;
let editor = null;
let questions = {};
let currentHintType = 'general';

// Success tracking functions
function getSuccessCount(questionId) {
    try {
        const counts = JSON.parse(localStorage.getItem('problem_success_counts') || '{}');
        return counts[questionId] || 0;
    } catch (e) {
        return 0;
    }
}

function incrementSuccessCount(questionId) {
    try {
        const counts = JSON.parse(localStorage.getItem('problem_success_counts') || '{}');
        counts[questionId] = (counts[questionId] || 0) + 1;
        localStorage.setItem('problem_success_counts', JSON.stringify(counts));
        return counts[questionId];
    } catch (e) {
        console.error('Error saving success count:', e);
        return 0;
    }
}

function getAllSuccessCounts() {
    try {
        return JSON.parse(localStorage.getItem('problem_success_counts') || '{}');
    } catch (e) {
        return {};
    }
}

// Helper function to create spinner
function createSpinner() {
    return '<span class="spinner"></span>';
}

// Helper function to set button loading state
function setButtonLoading(button, text, originalText) {
    if (!button) return;
    button.disabled = true;
    button.classList.add('loading');
    button.dataset.originalText = originalText || button.textContent;
    button.innerHTML = createSpinner() + text;
}

// Helper function to restore button state
function restoreButton(button) {
    if (!button) return;
    button.disabled = false;
    button.classList.remove('loading');
    if (button.dataset.originalText) {
        button.textContent = button.dataset.originalText;
        delete button.dataset.originalText;
    }
}

// Initialize CodeMirror editor
function initEditor() {
    editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
        lineNumbers: true,
        mode: 'python',
        theme: 'monokai',
        indentUnit: 4,
        indentWithTabs: false,
        lineWrapping: true,
        autoCloseBrackets: true,
        matchBrackets: true
    });
    
    // Make editor available globally for resize handler
    window.editor = editor;
    
    editor.on('change', () => {
        // Enable/disable buttons based on editor content
        const hasContent = editor.getValue().trim().length > 0;
        document.getElementById('runBtn').disabled = !hasContent || !currentQuestion;
        document.getElementById('compileBtn').disabled = !hasContent || !currentQuestion;
        document.getElementById('hintBtn').disabled = !currentQuestion;
    });
    
    // Refresh editor when panel is resized
    const resizeObserver = new ResizeObserver(() => {
        if (editor) {
            setTimeout(() => editor.refresh(), 100);
        }
    });
    
    const editorPanel = document.getElementById('editorPanel');
    if (editorPanel) {
        resizeObserver.observe(editorPanel);
    }
}

// Load questions from API
async function loadQuestions() {
    console.log('🔵 loadQuestions function called at', new Date().toISOString());
    const questionList = document.getElementById('questionList');
    
    if (!questionList) {
        console.error('❌ Question list element not found!');
        alert('ERROR: Question list element not found in DOM');
        return;
    }
    
    console.log('✓ Question list element found:', questionList);
    questionList.innerHTML = '<div class="loading">Fetching questions from API...</div>';
    
    try {
        console.log('🌐 Fetching /api/questions...');
        const response = await fetch('/api/questions', {
            cache: 'no-cache',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        console.log('📡 Response received:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        questions = data;
        
        console.log('📦 Data type:', typeof data, 'Is Array:', Array.isArray(data));
        console.log('📊 Questions count:', questions ? Object.keys(questions).length : 0);
        console.log('🔍 First 3 question IDs:', questions ? Object.keys(questions).slice(0, 3) : []);
        
        if (!questions || typeof questions !== 'object' || Object.keys(questions).length === 0) {
            console.error('❌ No questions in response!');
            questionList.innerHTML = '<div class="loading" style="color: red;">No questions available. API returned empty data.</div>';
            return;
        }
        
        console.log('✅ Questions loaded successfully! Rendering...');
        renderQuestionList();
        console.log('✅ renderQuestionList completed!');
    } catch (error) {
        console.error('Error loading questions:', error);
        questionList.innerHTML = 
            '<div class="loading" style="color: var(--error);">Error loading questions: ' + error.message + '<br>Please refresh the page.</div>';
    }
}

// Render question list
function renderQuestionList(filter = 'all') {
    console.log('renderQuestionList called with filter:', filter);
    const questionList = document.getElementById('questionList');
    if (!questionList) {
        console.error('Question list element not found!');
        return;
    }
    
    console.log('Questions object:', questions);
    console.log('Questions type:', typeof questions);
    console.log('Questions keys:', questions ? Object.keys(questions) : 'null');
    
    if (!questions || typeof questions !== 'object' || Object.keys(questions).length === 0) {
        console.warn('No questions available to render');
        questionList.innerHTML = '<div class="loading">No questions loaded yet...</div>';
        return;
    }
    
    const questionArray = Object.values(questions);
    console.log('Question array length:', questionArray.length);
    
    let filteredQuestions = questionArray;
    if (filter !== 'all') {
        filteredQuestions = questionArray.filter(q => 
            q && q.difficulty && q.difficulty.toLowerCase() === filter
        );
        console.log(`Filtered to ${filter}:`, filteredQuestions.length);
    }
    
    if (filteredQuestions.length === 0) {
        questionList.innerHTML = `<div class="loading">No ${filter} questions found.</div>`;
        return;
    }
    
    // Sort questions by title for better UX
    filteredQuestions.sort((a, b) => {
        const titleA = (a.title || '').toLowerCase();
        const titleB = (b.title || '').toLowerCase();
        return titleA.localeCompare(titleB);
    });
    
    try {
        // Get all success counts once
        const successCounts = getAllSuccessCounts();
        
        const html = filteredQuestions.map(q => {
            if (!q || !q.id) {
                console.warn('Invalid question:', q);
                return '';
            }
            const title = q.title || q.id || 'Untitled';
            const difficulty = (q.difficulty || 'Unknown').toLowerCase();
            const category = q.category || 'Uncategorized';
            const successCount = successCounts[q.id] || 0;
            
            // Escape HTML to prevent XSS
            const safeTitle = title.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            const safeCategory = category.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            
            return `
        <div class="question-item" data-id="${q.id}" onclick="selectQuestion('${q.id}')">
                    <div class="question-item-title">
                        ${safeTitle}
                        ${successCount > 0 ? `<span class="success-badge" title="Solved ${successCount} time${successCount > 1 ? 's' : ''}">✓ ${successCount}</span>` : ''}
                    </div>
            <div class="question-item-meta">
                        <span class="badge badge-${difficulty}">${q.difficulty || 'Unknown'}</span>
                        <span>${safeCategory}</span>
            </div>
        </div>
            `;
        }).filter(html => html).join('');
        
        console.log('Generated HTML length:', html.length);
        questionList.innerHTML = html;
        console.log('Questions rendered successfully!');
    } catch (error) {
        console.error('Error rendering questions:', error);
        questionList.innerHTML = '<div class="loading" style="color: var(--error);">Error rendering questions. Check console for details.</div>';
    }
}

// Select a question
async function selectQuestion(questionId) {
    try {
        console.log('📌 Selecting question:', questionId);
        
        // Update active state
        document.querySelectorAll('.question-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Find and highlight the clicked question
        const clickedItem = document.querySelector(`[data-id="${questionId}"]`);
        if (clickedItem) {
            clickedItem.classList.add('active');
        } else {
            console.warn('⚠️ Could not find question item to highlight');
        }
        
        // Load question details
        console.log('🌐 Fetching question details for:', questionId);
        const response = await fetch(`/api/questions/${questionId}`);
        if (!response.ok) {
            throw new Error(`Question not found (${response.status})`);
        }
        
        currentQuestion = await response.json();
        console.log('✅ Question loaded:', currentQuestion.title);
        
        renderQuestion();
        loadTemplate();
        
        // Enable buttons
        document.getElementById('hintBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;
        document.getElementById('runBtn').disabled = editor.getValue().trim().length === 0;
        
        console.log('✅ Question selection complete');
    } catch (error) {
        console.error('❌ Error loading question:', error);
        alert('Failed to load question: ' + error.message + '\n\nPlease try again or choose a different question.');
    }
}

// Update question panel title with success count
function updateQuestionPanelTitle(successCount) {
    if (!currentQuestion) return;
    
    const titleElement = document.querySelector('.question-title');
    if (!titleElement) return;
    
    const badgeHtml = successCount > 0 
        ? `<span class="success-badge" style="margin-left: 0.75rem;" title="Solved ${successCount} time${successCount > 1 ? 's' : ''}">✓ Solved ${successCount} time${successCount > 1 ? 's' : ''}</span>`
        : '';
    
    titleElement.innerHTML = `${currentQuestion.title}${badgeHtml}`;
}

// Render question details
function renderQuestion() {
    if (!currentQuestion) return;
    
    const panel = document.getElementById('questionPanel');
    
    let examplesHtml = '';
    if (currentQuestion.examples) {
        examplesHtml = currentQuestion.examples.map((ex, idx) => `
            <div class="example">
                <div class="example-label">Example ${idx + 1}:</div>
                <div class="example-code">
                    <strong>Input:</strong> ${JSON.stringify(ex.input)}<br>
                    <strong>Output:</strong> ${JSON.stringify(ex.output)}<br>
                    ${ex.explanation ? `<strong>Explanation:</strong> ${ex.explanation}` : ''}
                </div>
            </div>
        `).join('');
    }
    
    let constraintsHtml = '';
    if (currentQuestion.constraints) {
        constraintsHtml = `
            <div class="constraints">
                <h4>Constraints:</h4>
                <ul>
                    ${currentQuestion.constraints.map(c => `<li>${c}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    const successCount = getSuccessCount(currentQuestion.id);
    
    panel.innerHTML = `
        <div class="resize-handle resize-handle-bottom" data-target="questionPanel"></div>
        <div class="question-title">
            ${currentQuestion.title}
            ${successCount > 0 ? `<span class="success-badge" style="margin-left: 0.75rem;" title="Solved ${successCount} time${successCount > 1 ? 's' : ''}">✓ Solved ${successCount} time${successCount > 1 ? 's' : ''}</span>` : ''}
        </div>
        <div class="question-meta">
            <span class="badge badge-${currentQuestion.difficulty.toLowerCase()}">${currentQuestion.difficulty}</span>
            <span>${currentQuestion.category}</span>
        </div>
        <div class="question-description">${currentQuestion.description}</div>
        ${examplesHtml ? `<div class="question-examples">${examplesHtml}</div>` : ''}
        ${constraintsHtml}
    `;
}

// Load template code
function loadTemplate() {
    if (currentQuestion && currentQuestion.template) {
        editor.setValue(currentQuestion.template);
    }
}

// Execute code immediately (runs code with examples or simple test)
async function compileCode() {
    if (!currentQuestion) return;
    
    const code = editor.getValue();
    const resultsPanel = document.getElementById('resultsContent');
    const compileBtn = document.getElementById('compileBtn');
    
    // Show loading state
    setButtonLoading(compileBtn, 'Executing...', '⚡ Execute Code');
    resultsPanel.innerHTML = '<div class="loading">⚡ Executing code... Please wait.</div>';
    
    try {
        // First, do a quick syntax check
        const compileResponse = await fetch('/api/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                question_id: currentQuestion.id
            })
        });
        
        const compileResult = await compileResponse.json();
        
        if (!compileResult.success) {
            // Show syntax error
            resultsPanel.innerHTML = `
                <div class="error-message">
                    <strong>❌ Syntax Error:</strong><br>
                    <pre style="margin-top: 0.5rem; white-space: pre-wrap;">${compileResult.error || 'Unknown error'}</pre>
                </div>
            `;
            return;
        }
        
        // If syntax is OK, execute the code
        const executeResponse = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                question_id: currentQuestion.id
            })
        });
        
        if (!executeResponse.ok) {
            const errorText = await executeResponse.text();
            throw new Error(`Server error: ${executeResponse.status} - ${errorText.substring(0, 200)}`);
        }
        
        const result = await executeResponse.json();
        
        if (result.errors && result.errors.length > 0) {
            let errorHtml = result.errors.map(err => `
                <div class="error-message">
                    <strong>Runtime Error:</strong><br>
                    <pre style="margin-top: 0.5rem; white-space: pre-wrap;">${err.error || 'Unknown error'}</pre>
                </div>
            `).join('');
            
            resultsPanel.innerHTML = errorHtml + (result.results || []).map(r => renderExecutionResult(r)).join('');
        } else if (result.results && result.results.length > 0) {
            resultsPanel.innerHTML = `
                <div style="padding: 0.5rem; background: rgba(16, 185, 129, 0.1); 
                            border-left: 3px solid var(--success-color); border-radius: 0.5rem; color: var(--success-color); margin-bottom: 1rem;">
                    <strong>✅ Code executed successfully!</strong>
                </div>
            ` + result.results.map(r => renderExecutionResult(r)).join('');
        } else if (result.error) {
            resultsPanel.innerHTML = `
                <div class="error-message">
                    <strong>Error:</strong><br>
                    ${result.error}
                </div>
            `;
        } else {
            resultsPanel.innerHTML = '<div class="placeholder">Code executed but no output.</div>';
        }
    } catch (error) {
        console.error('Execute error:', error);
        resultsPanel.innerHTML = `
            <div class="error-message">
                <strong>❌ Error Executing Code</strong><br><br>
                ${error.message}<br><br>
                <small>Please check your code for syntax errors and try again.</small>
            </div>
        `;
    } finally {
        // Restore button state
        restoreButton(compileBtn);
    }
}

// Render execution result (for immediate execution)
function renderExecutionResult(result) {
    const consoleOutput = result.console_output && result.console_output.trim() 
        ? `<div class="console-output">
                <strong>📄 Console Output:</strong>
                <pre>${escapeHtml(result.console_output)}</pre>
           </div>` 
        : '';
    
    return `
        <div class="test-result passed" style="margin-top: 1rem;">
            <div class="test-result-header">
                ✅ Execution Result
            </div>
            <div class="test-result-details">
                <strong>Input:</strong> ${JSON.stringify(result.input)}<br>
                <strong>Output:</strong> <code style="color: var(--success-color);">${JSON.stringify(result.output)}</code>
                ${result.expected !== null && result.expected !== undefined ? `<br><strong>Expected:</strong> ${JSON.stringify(result.expected)}` : ''}
                ${consoleOutput}
            </div>
        </div>
    `;
}

// Run tests
async function runTests() {
    if (!currentQuestion) return;
    
    const code = editor.getValue();
    const resultsPanel = document.getElementById('resultsContent');
    const runBtn = document.getElementById('runBtn');
    
    // Show loading state
    setButtonLoading(runBtn, 'Running Tests...', '▶️ Run Tests');
    resultsPanel.innerHTML = '<div class="loading">🔄 Running tests... Please wait.</div>';
    
    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                test_cases: currentQuestion.test_cases || [],
                question_id: currentQuestion.id
            })
        });
        
        // Check if response is OK
        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { error: await response.text() };
            }
            
            // Handle specific error cases
            if (response.status === 400 && errorData.error) {
                let errorHtml = `
                    <div class="error-message">
                        <strong>❌ Cannot Run Tests</strong><br><br>
                        ${errorData.error}<br>
                `;
                if (errorData.details) {
                    errorHtml += `<br><small>${errorData.details}</small>`;
                }
                if (errorData.suggestion) {
                    errorHtml += `<br><br><strong>💡 Suggestion:</strong> ${errorData.suggestion}`;
                }
                errorHtml += `</div>`;
                resultsPanel.innerHTML = errorHtml;
            } else {
                throw new Error(`Server error: ${response.status} - ${errorData.error || 'Unknown error'}`);
            }
            return;
        }
        
        const result = await response.json();
        
        if (result.errors && result.errors.length > 0) {
            let errorHtml = result.errors.map(err => `
                <div class="error-message">
                    <strong>❌ Test Case ${err.test_case || 'Error'}:</strong><br>
                    <pre style="margin-top: 0.5rem; white-space: pre-wrap;">${err.error || 'Unknown error'}</pre>
                </div>
            `).join('');
            
            const resultsHtml = result.results && result.results.length > 0 
                ? renderTestResults(result.results, result.errors)
                : '';
            resultsPanel.innerHTML = errorHtml + resultsHtml;
        } else if (result.results && result.results.length > 0) {
            resultsPanel.innerHTML = renderTestResults(result.results, result.errors || []);
            
            if (result.all_passed) {
                // Increment success count
                if (currentQuestion && currentQuestion.id) {
                    const newCount = incrementSuccessCount(currentQuestion.id);
                    // Update the question list to show new count
                    renderQuestionList(document.querySelector('.filter-btn.active')?.getAttribute('data-filter') || 'all');
                    // Update the question panel title
                    updateQuestionPanelTitle(newCount);
                }
                
                const successCount = currentQuestion ? getSuccessCount(currentQuestion.id) : 0;
                resultsPanel.innerHTML += `
                    <div style="margin-top: 1rem; padding: 1rem; background: rgba(16, 185, 129, 0.1); 
                                border-left: 3px solid var(--success); border-radius: 0.5rem; color: var(--success);">
                        🎉 All tests passed! Great job!
                        ${successCount > 1 ? `<br><small style="opacity: 0.8;">✅ Solved successfully ${successCount} time${successCount > 1 ? 's' : ''}!</small>` : ''}
                    </div>
                `;
            }
        } else {
            resultsPanel.innerHTML = '<div class="placeholder">No test results available. Check that test cases are configured for this question.</div>';
        }
    } catch (error) {
        console.error('Error running tests:', error);
        resultsPanel.innerHTML = `
            <div class="error-message">
                <strong>❌ Error Running Tests</strong><br><br>
                ${error.message}<br><br>
                <small>Please check your code for syntax errors and try again.</small>
            </div>
        `;
    } finally {
        // Restore button state
        restoreButton(runBtn);
    }
}

// Render test results with summary
function renderTestResults(results, errors) {
    if (!results || results.length === 0) {
        return '';
    }
    
    const passed = results.filter(r => r.passed).length;
    const total = results.length;
    const allPassed = passed === total && errors.length === 0;
    const allFailed = passed === 0;
    
    let summaryClass = 'partial';
    let summaryIcon = '⚠️';
    let summaryText = `${passed}/${total} tests passed`;
    
    if (allPassed) {
        summaryClass = 'passed';
        summaryIcon = '✅';
        summaryText = `✅ ${total}/${total} tests passed`;
    } else if (allFailed) {
        summaryClass = 'failed';
        summaryIcon = '❌';
        summaryText = `❌ ${total}/${total} tests failed`;
    }
    
    let html = `
        <div class="test-summary ${summaryClass}">
            ${summaryIcon} ${summaryText}
        </div>
    `;
    
    results.forEach(result => {
        html += renderTestResult(result);
    });
    
    return html;
}

// Render test result
function renderTestResult(result) {
    const statusClass = result.passed ? 'passed' : 'failed';
    const statusIcon = result.passed ? '✅' : '❌';
    const statusText = result.passed ? 'Passed' : 'Failed';
    
    const testId = `test-${result.test_case}`;
    const inputStr = JSON.stringify(result.input, null, 2);
    const expectedStr = JSON.stringify(result.expected, null, 2);
    const outputStr = JSON.stringify(result.output, null, 2);
    
    // Add console output if available
    const consoleOutput = result.console_output && result.console_output.trim() 
        ? `<div class="console-output" style="margin-top: 1rem;">
                <strong>📄 Console Output:</strong>
                <pre>${escapeHtml(result.console_output)}</pre>
           </div>` 
        : '';
    
    // Add error message if available
    const errorMessage = result.error 
        ? `<div style="margin-top: 0.5rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.1); border-radius: 0.25rem;">
                <strong>Error:</strong><br>
                <pre style="margin: 0.5rem 0 0 0; color: var(--error);">${escapeHtml(result.error)}</pre>
           </div>`
        : '';
    
    return `
        <div class="test-result ${statusClass}">
            <div class="test-result-header">
                <span>${statusIcon} Test Case ${result.test_case}: ${statusText}</span>
                <button class="copy-test-btn" onclick="copyTestCase('${testId}', event)" title="Copy test case">
                    📋 Copy
                </button>
            </div>
            <div class="test-result-details" id="${testId}">
                <div style="margin-bottom: 0.5rem;">
                    <strong>Input:</strong><br>
                    <code>${inputStr}</code>
                </div>
                ${result.expected !== undefined && result.expected !== null ? `
                <div style="margin-bottom: 0.5rem;">
                    <strong>Expected:</strong><br>
                    <code>${expectedStr}</code>
                </div>
                ` : ''}
                <div>
                    <strong>Got:</strong><br>
                    <code style="color: ${result.passed ? 'var(--success)' : 'var(--error)'};">${outputStr}</code>
                </div>
                ${errorMessage}
                ${consoleOutput}
            </div>
        </div>
    `;
}

// Copy test case to clipboard
function copyTestCase(testId, event) {
    const element = document.getElementById(testId);
    if (!element) return;
    
    // Get the test case data in a readable format
    const details = element.querySelectorAll('div');
    let text = '';
    details.forEach(div => {
        text += div.textContent.trim() + '\n';
    });
    
    navigator.clipboard.writeText(text.trim()).then(() => {
        // Show feedback - find the button that triggered this
        const btn = event ? event.target : document.querySelector(`button[onclick*="${testId}"]`);
        if (btn && btn.classList.contains('copy-test-btn')) {
            const originalText = btn.textContent;
            btn.textContent = '✓ Copied!';
            btn.style.color = 'var(--success)';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.color = '';
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Get hint with timeout and better error handling
async function getHint(hintType = 'general') {
    if (!currentQuestion) {
        console.log('No question selected');
        return;
    }
    
    console.log(`Getting ${hintType} hint for:`, currentQuestion.title);
    currentHintType = hintType;
    const hintContent = document.getElementById('hintContent');
    const hintPanel = document.getElementById('hintPanel');
    
    // Show loading state with timeout warning
    const hintBtn = document.getElementById('hintBtn');
    setButtonLoading(hintBtn, 'Generating Hint...', '💡 Get Hint');
    
    let timeoutWarning = null;
    hintContent.innerHTML = '<div class="loading">🤔 Generating hint... (this may take 15-30 seconds on first request)</div>';
    hintPanel.classList.add('visible');
    
    // Set up timeout warning after 10 seconds
    timeoutWarning = setTimeout(() => {
        if (hintContent.innerHTML.includes('Generating hint')) {
            hintContent.innerHTML = '<div class="loading">🤔 Still generating... LLM is processing (this can take up to 30 seconds)</div>';
        }
    }, 10000);
    
    try {
        console.log('Fetching hint from API...');
        
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 45000); // 45 second timeout
        
        const response = await fetch('/api/hint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: currentQuestion,
                code: editor.getValue(),
                hint_type: hintType
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        if (timeoutWarning) clearTimeout(timeoutWarning);
        
        // Restore hint button
        restoreButton(hintBtn);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error: ${response.status} - ${errorText.substring(0, 200)}`);
        }
        
        const result = await response.json();
        console.log('Hint received:', result);
        
        if (result && result.hint) {
            // Format hint with better HTML
            const formattedHint = result.hint
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                .replace(/```python\n([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
                .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
                .split('\n')
                .map(line => {
                    const trimmed = line.trim();
                    if (!trimmed) return '';
                    if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
                        return `<li>${trimmed.substring(2)}</li>`;
                    }
                    if (trimmed.startsWith('1. ') || trimmed.match(/^\d+\. /)) {
                        return `<li>${trimmed.replace(/^\d+\. /, '')}</li>`;
                    }
                    return `<p>${trimmed}</p>`;
                })
                .join('');
            
            hintContent.innerHTML = `<div class="hint-message">${formattedHint}</div>`;
            console.log('✅ Hint displayed successfully');
        } else {
            console.log('No hint in response, showing fallback');
            hintContent.innerHTML = `
                <div class="hint-message">
                    <strong>💡 Hint:</strong><br><br>
                    Consider these questions:<br>
                    • What data structure fits this problem?<br>
                    • Can you solve it in O(n) time?<br>
                    • Have you seen a similar pattern before?
                </div>
            `;
        }
    } catch (error) {
        if (timeoutWarning) clearTimeout(timeoutWarning);
        restoreButton(hintBtn);
        console.error('❌ Error getting hint:', error);
        
        // Check if it's a timeout error
        if (error.name === 'AbortError' || error.message.includes('timeout')) {
            hintContent.innerHTML = `
                <div class="error-message">
                    <strong>⏱️ Request Timeout</strong><br><br>
                    The hint generation took too long. This can happen on the first request when the LLM is loading.<br><br>
                    <strong>Try again:</strong> The LLM should be loaded now, so subsequent hints will be faster.<br><br>
                    <button class="btn btn-hint-small" onclick="getHint('${hintType}')" style="margin-top: 0.5rem;">🔄 Retry</button>
                </div>
            `;
        } else {
            // Other errors - show fallback hint
        hintContent.innerHTML = `
            <div class="hint-message">
                <strong>💡 Hint:</strong><br><br>
                Break down the problem:<br>
                1. Understand the input and output<br>
                2. Think about edge cases<br>
                3. Consider what data structure would help<br>
                    4. Start with a brute force solution, then optimize<br><br>
                    <small style="opacity: 0.7;">Note: AI hint generation encountered an error. Showing fallback hint.</small>
            </div>
        `;
        }
    }
}

// Reset code
function resetCode() {
    if (currentQuestion) {
        loadTemplate();
    }
}

// Clear results
function clearResults() {
    document.getElementById('resultsContent').innerHTML = 
        '<p class="placeholder">Run your code to see test results here.</p>';
}

// Close hint panel
function closeHintPanel() {
    document.getElementById('hintPanel').classList.remove('visible');
}

// Show solution code
async function showSolution() {
    if (!currentQuestion) {
        console.log('No question selected');
        return;
    }
    
    console.log('Fetching solution for:', currentQuestion.title);
    const hintContent = document.getElementById('hintContent');
    const hintPanel = document.getElementById('hintPanel');
    const showSolutionBtn = document.getElementById('showSolutionBtn');
    
    // Show loading state
    setButtonLoading(showSolutionBtn, 'Loading...', '💻 Show Solution');
    hintContent.innerHTML = '<div class="loading">🔍 Loading solution...</div>';
    hintPanel.classList.add('visible');
    
    try {
        const response = await fetch('/api/solution', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: currentQuestion
            })
        });
        
        restoreButton(showSolutionBtn);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Solution received:', result);
        
        if (result && result.available && result.solution) {
            // Format solution with metadata
            const solutionHTML = `
                <div class="solution-container">
                    <div class="solution-header">
                        <h4>💻 Optimal Solution</h4>
                        <span class="solution-warning">⚠️ Viewing the solution - Try solving it yourself first!</span>
                    </div>
                    
                    <div class="solution-meta">
                        <div class="meta-item">
                            <strong>Approach:</strong> ${result.approach}
                        </div>
                        ${result.time_complexity ? `
                        <div class="meta-item">
                            <strong>Time Complexity:</strong> ${result.time_complexity}
                        </div>
                        ` : ''}
                        ${result.space_complexity ? `
                        <div class="meta-item">
                            <strong>Space Complexity:</strong> ${result.space_complexity}
                        </div>
                        ` : ''}
                    </div>
                    
                    ${result.explanation ? `
                    <div class="solution-explanation">
                        <strong>📚 Detailed Explanation:</strong>
                        ${formatExplanation(result.explanation)}
                    </div>
                    ` : ''}
                    
                    <div class="solution-code">
                        <div class="code-header">
                            <strong>Solution Code:</strong>
                            <button class="btn-copy-solution" onclick="copySolutionCode()">📋 Copy</button>
                        </div>
                        <pre><code class="language-python" id="solutionCode">${escapeHtml(result.solution)}</code></pre>
                    </div>
                    
                    <div class="solution-actions">
                        <button class="btn btn-hint-small" onclick="copySolutionToEditor()">
                            📝 Copy to Editor
                        </button>
                        <button class="btn btn-hint-small" onclick="closeHintPanel()">
                            ✓ Got It
                        </button>
                    </div>
                </div>
            `;
            
            hintContent.innerHTML = solutionHTML;
            console.log('✅ Solution displayed successfully');
        } else {
            // Solution not available
            hintContent.innerHTML = `
                <div class="hint-message">
                    <strong>💡 Solution Not Available</strong><br><br>
                    ${result.message || 'The solution for this problem is not yet in the knowledge base.'}<br><br>
                    Try solving it step by step using the hint buttons!
                </div>
            `;
        }
    } catch (error) {
        restoreButton(showSolutionBtn);
        console.error('❌ Error getting solution:', error);
        hintContent.innerHTML = `
            <div class="error-message">
                <strong>❌ Error Loading Solution</strong><br><br>
                Failed to load the solution. Please try again.<br><br>
                <button class="btn btn-hint-small" onclick="showSolution()">🔄 Retry</button>
            </div>
        `;
    }
}

// Copy solution code to clipboard
function copySolutionCode() {
    const codeElement = document.getElementById('solutionCode');
    if (!codeElement) return;
    
    const code = codeElement.textContent;
    navigator.clipboard.writeText(code).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Copy solution to editor
function copySolutionToEditor() {
    const codeElement = document.getElementById('solutionCode');
    if (!codeElement || !editor) return;
    
    const code = codeElement.textContent;
    
    // Ask for confirmation
    if (confirm('Replace your current code with the solution?\n\nYour current code will be lost.')) {
        editor.setValue(code);
        closeHintPanel();
        alert('✅ Solution copied to editor!');
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Format explanation with proper HTML structure
function formatExplanation(explanation) {
    if (!explanation) return '';
    
    // Split by double newlines to get sections
    let parts = explanation.split('\n\n');
    let html = '';
    
    for (let part of parts) {
        part = part.trim();
        if (!part) continue;
        
        // Check if it's Algorithm Steps section
        if (part.includes('**Algorithm Steps:**')) {
            html += '<div class="explanation-section">';
            part = part.replace(/\*\*Algorithm Steps:\*\*/g, '<strong>🔢 Algorithm Steps:</strong>');
            
            // Format numbered steps
            part = part.replace(/(\d+\.\s+[^\n]+)/g, '<div class="step-item">$1</div>');
            html += '<p>' + part + '</p></div>';
        }
        // Check if it's Key Insight section
        else if (part.includes('**Key Insight:**')) {
            html += '<div class="explanation-section insight-section">';
            part = part.replace(/\*\*Key Insight:\*\*/g, '<strong>💡 Key Insight:</strong>');
            html += '<p>' + part + '</p></div>';
        }
        // Regular paragraph
        else {
            // Format bold text
            part = part.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            // Format code-like text (backticks)
            part = part.replace(/`([^`]+)`/g, '<code>$1</code>');
            html += '<p>' + part + '</p>';
        }
    }
    
    return html || '<p>' + escapeHtml(explanation).replace(/\n/g, '<br>') + '</p>';
}

// Copy code to clipboard
function copyCode() {
    if (!editor) return;
    
    const code = editor.getValue();
    navigator.clipboard.writeText(code).then(() => {
        const btn = document.getElementById('copyCodeBtn');
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('copied');
        }, 2000);
    });
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Check if CodeMirror editor is focused
        const editorFocused = editor && editor.hasFocus();
        
        // Don't trigger shortcuts when typing in input fields (but allow in editor)
        if (!editorFocused && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) {
            return;
        }
        
        const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
        const ctrlKey = isMac ? e.metaKey : e.ctrlKey;
        
        // Ctrl/Cmd + Enter: Run Tests
        if (ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            const runBtn = document.getElementById('runBtn');
            if (!runBtn.disabled) {
                runTests();
            }
            return;
        }
        // Ctrl/Cmd + E: Execute Code
        if (ctrlKey && e.key === 'e') {
            e.preventDefault();
            const compileBtn = document.getElementById('compileBtn');
            if (!compileBtn.disabled) {
                compileCode();
            }
            return;
        }
        // Ctrl/Cmd + R: Reset Code (only when not in editor to avoid browser refresh)
        if (ctrlKey && e.key === 'r' && !editorFocused) {
            e.preventDefault();
            const resetBtn = document.getElementById('resetBtn');
            if (!resetBtn.disabled) {
                resetCode();
            }
            return;
        }
        // Ctrl/Cmd + H: Get Hint
        if (ctrlKey && e.key === 'h') {
            e.preventDefault();
            const hintBtn = document.getElementById('hintBtn');
            if (!hintBtn.disabled) {
                getHint('general');
            }
            return;
        }
        // Ctrl/Cmd + Shift + C: Copy Code (use Shift to avoid conflict with normal copy)
        if (ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            copyCode();
            return;
        }
    });
}

// Test that JavaScript file is loaded
console.log('🚀 APP.JS LOADED - Version: ' + new Date().getTime());

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== 🎬 APP INITIALIZING ===');
    console.log('Timestamp:', new Date().toISOString());
    
    // Initialize editor
    initEditor();
    console.log('✓ Editor initialized');
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
    console.log('✓ Keyboard shortcuts setup');
    
    // Load questions
    loadQuestions();
    console.log('✓ Load questions called');
    
    // Setup button event listeners
    const compileBtn = document.getElementById('compileBtn');
    const runBtn = document.getElementById('runBtn');
    const hintBtn = document.getElementById('hintBtn');
    const resetBtn = document.getElementById('resetBtn');
    const clearResultsBtn = document.getElementById('clearResultsBtn');
    const closeHintBtn = document.getElementById('closeHintBtn');
    const copyCodeBtn = document.getElementById('copyCodeBtn');
    const showSolutionBtn = document.getElementById('showSolutionBtn');
    
    if (compileBtn) compileBtn.addEventListener('click', compileCode);
    if (runBtn) runBtn.addEventListener('click', runTests);
    if (hintBtn) hintBtn.addEventListener('click', () => getHint('general'));
    if (resetBtn) resetBtn.addEventListener('click', resetCode);
    if (clearResultsBtn) clearResultsBtn.addEventListener('click', clearResults);
    if (closeHintBtn) closeHintBtn.addEventListener('click', closeHintPanel);
    if (copyCodeBtn) copyCodeBtn.addEventListener('click', copyCode);
    if (showSolutionBtn) showSolutionBtn.addEventListener('click', showSolution);
    
    console.log('✓ Button listeners attached');
    
    // Setup hint type buttons
    document.querySelectorAll('[data-hint-type]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const hintType = e.target.getAttribute('data-hint-type');
            if (hintType) getHint(hintType);
        });
    });
    
    // Setup filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    console.log('Found filter buttons:', filterButtons.length);
    filterButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            const filter = e.target.getAttribute('data-filter') || 'all';
            console.log('Filter clicked:', filter);
            renderQuestionList(filter);
        });
    });
    
    console.log('✓ Filter buttons setup');
    console.log('=== APP INITIALIZED ===');
});

// Make functions globally available for inline onclick handlers
window.selectQuestion = selectQuestion;
window.copyTestCase = copyTestCase;

