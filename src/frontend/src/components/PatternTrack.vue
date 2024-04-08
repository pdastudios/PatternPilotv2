<template>
    <div id="app" class="row">
        <div class="col">
            <h1>THIS IS THE TRACK ONE</h1>
        </div>
        <div class="col">
            <form @submit.prevent="submitShape()" >
                <div class="form-group col">
                    <input type="text" class="form-control col-3 mx-2" placeholder="Enter Shape Name" v-model="shape.name">
                    <button class="btn btn-success">Submit</button>
                </div>
            </form>
        </div>

        <div class="col">
            <div v-if="warningMessage" class="alert alert-warning" role="alert">
                <strong>Warning!</strong> {{ warningMessage }}
            </div>

            <div class="row">
                <div class="col">{{ currentResultMessage }}</div>
                <div class="col">{{ lastResultMessage }}</div>
                <div class="col">{{ validatedValueMessage }}</div>
            </div>

            <form @submit.prevent="submitRound()">
                <div class="form-group col">
                    <input type="text" class="form-control col-3 mx-2" placeholder="Enter Formula | Example: sc,sc,sc" v-model="round.formula" @input="updateResult(); formatUserInput()" :class="{ 'is-invalid': round.formula && !calculateFormula(round.formula), 'is-valid': round.formula && calculateFormula(round.formula) }">
                    <input type="number" class="form-control col-3 mx-2" placeholder="Shape ID" v-model.number="round.shape">
                    <input type="text" class="form-control col-3 mx-2" placeholder="Enter Comment | Example: add this in magic ring" v-model="round.comment">
                    <button class="btn btn-success">Submit</button>
                </div>
            </form>

            <div class="card m-3 p-5" v-for="shape in shapes" :key="shape.id">
                <h3 @click="toggleAccordion(shape.id)">{{ shape.name }}</h3>
                    <div v-show="isShapeOpen(shape.id)">
                    <table class="table ">
                        <thead>
                            <th>Round</th>
                            <th>Pattern</th>
                            <th>Result</th>
                            <th>Comment</th>
                        </thead>
                        <tbody>
                            <tr v-for="(round, index) in getRoundsForShape(shape.id)" :key="round.id" @dblclick="$data.round=round">
                                <td>{{ index + 1 }}</td>
                                <td>{{ round.formula }}</td>
                                <td>{{ round.result }}</td>
                                <td>{{ round.comment }}</td>
                                <td>
                                    <button class="btn btn-outline-danger btn-sm mx-1" @click="deleteRound(round)">x</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>
</template>

<script>

//import draggable from 'vuedraggable';

export default {
    name: 'PatternTrack',
    data() {
        return {
            shapes: [],
            shape: {
                name:'',
            },
            rounds: [],
            round: {
                formula: '', // Default value for the formula
                shape: '', // Default value for the shape
                comment: '',
            },
            pattern: '',
            currentResultMessage: '', // Initialize with Current Result: 0
            warningMessage:'',
            validatedValueMessage: '', // Initialize with Validated Value: 0
            lastResultMessage: '',
            openShapeId: null, 
        };
    },

    async created() {
        await this.getShapes();
        await this.getRounds();
        //await this.fetchPattern();
    },

    methods: {
        async submitShape() {
            // If the validated value matches the last result for the shape, or if this is the first result for this shape, proceed with form submission
            if (this.shape.id === undefined) {
                this.createShape(); // Pass the currentResult to createRound
            } else {
                this.editShape(); // Pass the currentResult to editRound
            }
        },

        async createShape() {
            try {
                
                // Send the request to create the round
                const response = await fetch('http://127.0.0.1:8000/shapes/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: this.shape.name,
                    })
                });

                // Check if the request was successful
                if (!response.ok) {
                    throw new Error('Failed to create shape');
                }

                // Refresh the rounds data
                await this.getShapes();
                await this.resetValues();
            } catch (error) {
                console.error('Error creating round:', error);
            }
        },

        navigateToOtherPage() {
            // Replace 'http://example.com' with the URL you want to navigate to
            window.location.href = 'track.html';
        },

        async submitRound() {
            const { isValid, currentResult } = await this.calculateFormula(this.round.formula);
            if (!isValid) {
                this.warningMessage = 'Invalid formula';
                this.currentResultMessage = '';
                return;
            }

            // Calculate the validated value for the current formula
            const validatedValue = this.calculateValidatedValue(this.round.formula);

            // Find the last round for the current shape
            const roundsForCurrentShape = this.rounds.filter(round => round.shape === this.round.shape);

            const lastRound = roundsForCurrentShape[roundsForCurrentShape.length - 1];

            // If there is a last round for the current shape, compare the validated value to its result
            if (lastRound && validatedValue !== lastRound.result) {
                this.warningMessage = `The current validated value (${validatedValue}) does not match the last result for this shape (${lastRound.result}).`;
                this.lastResultMessage = `Last result: ${lastRound.result}`;
                // You might want to stop the form submission or handle it differently here
            } else {
                this.warningMessage = '';
                this.lastResultMessage = `Last result: N/A`;
            }

            // If the validated value matches the last result for the shape, or if this is the first result for this shape, proceed with form submission
            if (this.round.id === undefined) {
                this.createRound(currentResult); // Pass the currentResult to createRound
            } else {
                this.editRound(currentResult); // Pass the currentResult to editRound
            }
            this.warningMessage = ''; // Clear the validation message
        },


        
        async getRounds() {
            try {
                const response = await fetch('http://127.0.0.1:8000/track/');
                if (!response.ok) {
                    throw new Error('Failed to fetch round data');
                }
                const data = await response.json();
                this.rounds = [];
                let roundNumber = 0; // Initialize round number for the current shape
                let currentShapeId = null; // Initialize current shape ID

                for (const round of data) {
                    // If the shape ID changes, reset the round number to 1
                    if (round.shape !== currentShapeId) {
                        roundNumber = 1;
                        currentShapeId = round.shape;
                    } else {
                        roundNumber++; // Increment round number for the current shape
                    }

                    // Validate the formula and calculate the result
                    //const { isValid, currentResult } = await this.calculateFormula(round.formula);
                    
                    // Push round data with updated result and round number
                    this.rounds.push({
                        ...round,
                        number: roundNumber,
                        result: round.result,
                        //isValid: isValid
                    });
                }
            } catch (error) {
                console.error('Error fetching round data:', error);
            }
        },


        async getShapes() {
            try {
                const response = await fetch('http://127.0.0.1:8000/shapes/');
                if (!response.ok) {
                    throw new Error('Failed to fetch round data');
                }
                this.shapes = await response.json();
            } catch (error) {
                console.error('Error fetching round data:', error);
            }
        },


        async calculateFormula(formula) {

            let currentResult = 0;
            let isValid = false;
            if (formula && formula.trim() !== '') {
                // Split formula by commas outside of parentheses
                const parts = formula.split(/,(?![^(]*\))/).map(part => part.trim());

                parts.forEach(part => {
                    const match = part.match(/^\((.*)\)(?:\*(\d+))?$/);
                    if (match) {
                        const subParts = match[1].split(',').map(subPart => subPart.trim());
                        const repetition = parseInt(match[2], 10) || 1;

                        subParts.forEach(subPart => {
                            const subMatch = subPart.match(/^(\d+)?([a-zA-Z]+)$/);
                            if (subMatch) {
                                const subRepetition = parseInt(subMatch[1], 10) || 1;
                                const abbreviation = subMatch[2].toLowerCase();

                                // Update result based on abbreviation
                                if (abbreviation === 'sc' || abbreviation === 'slst' || abbreviation === 'ch'  || abbreviation === 'dec') {
                                    currentResult += subRepetition * repetition;
                                } else if (abbreviation === 'inc') {
                                    currentResult += 2 * subRepetition * repetition;
                                } else if (abbreviation === 'tinc') {
                                    currentResult += 3 * subRepetition * repetition;
                                } 
                            }
                        });
                    } else {
                        const singleMatch = part.match(/^(\d+)?([a-zA-Z]+)$/);
                        if (singleMatch) {
                            const repetition = parseInt(singleMatch[1], 10) || 1; // default repetition to 1 if not specified
                            const abbreviation = singleMatch[2].toLowerCase();

                            // Update result based on abbreviation
                            if (abbreviation === 'sc' || abbreviation === 'slst' || abbreviation === 'ch'  || abbreviation === 'dec') {
                                currentResult += repetition;
                            } else if (abbreviation === 'inc') {
                                currentResult += 2 * repetition;
                            } else if (abbreviation === 'tinc') {
                                currentResult += 3 * repetition;
                            }
                        }
                    }
                });

                // Ensure the result is not negative
                currentResult = Math.max(currentResult, 0);

                // Validation logic (add your own validation conditions here)
                if (currentResult >= 0) {
                    // Formula is valid
                    isValid = true;
                    this.currentResultMessage = 'Current result: ' + currentResult;
                    return { isValid, currentResult };
                } else {
                    // Formula is invalid
                    this.warningMessage = 'Invalid formula: Result cannot be negative';
                    this.currentResultMessage = 'Current Result: Syntax Error';
                    return false;
                }
            } else {
                // Formula is empty
                this.warningMessage = 'Formula cannot be empty';
                this.currentResultMessage = 'Current Result: N/A';
                return false;
            }
        },

        calculateValidatedValue(formula) {
            let validatedValue = 0;
            if (formula && formula.trim() !== '') {
                // Split formula by commas outside of parentheses
                const parts = formula.split(/,(?![^(]*\))/).map(part => part.trim());

                parts.forEach(part => {
                    const match = part.match(/^\((.*)\)(?:\*(\d+))?$/);
                    if (match) {
                        const subParts = match[1].split(',').map(subPart => subPart.trim());
                        const repetition = parseInt(match[2], 10) || 1;

                        subParts.forEach(subPart => {
                            const subMatch = subPart.match(/^(\d+)?([a-zA-Z]+)$/);
                            if (subMatch) {
                                const subRepetition = parseInt(subMatch[1], 10) || 1;
                                const abbreviation = subMatch[2].toLowerCase();

                                // Update validated value based on abbreviation
                                if (['sc', 'slst', 'ch', 'inc', 'tinc'].includes(abbreviation)) {
                                    validatedValue += subRepetition * repetition;
                                } else if (abbreviation === 'dec') {
                                    validatedValue += 2 * subRepetition * repetition;
                                }
                            }
                        });
                    } else {
                        const singleMatch = part.match(/^(\d+)?([a-zA-Z]+)$/);
                        if (singleMatch) {
                            const repetition = parseInt(singleMatch[1], 10) || 1;
                            const abbreviation = singleMatch[2].toLowerCase();

                            // Update validated value based on abbreviation
                            if (['sc', 'slst', 'ch', 'inc', 'tinc'].includes(abbreviation)) {
                                validatedValue += repetition;
                            } else if (abbreviation === 'dec') {
                                validatedValue += 2 * repetition;
                            }
                        }
                    }
                });
            }

            return validatedValue;
        },

        validateFormData() {
            // Perform validation checks on form data
            if (!this.round.formula || !this.round.shape) {
                console.error('Please fill in all required fields.');
                return false;
            }

            // Validate the formula
            const isFormulaValid = this.calculateFormula(this.round.formula);
            if (!isFormulaValid) {
                console.error('Invalid formula.');
                return false;
            }

            // Add more validation checks if needed
            return true;
        },

        getRoundsForShape(shapeId) {
            return this.rounds.filter(round => round.shape === shapeId);
        },

        updateResult() {
            if (this.round.formula) {
                // Calculate the validated value for the current formula
                const validatedValue = this.calculateValidatedValue(this.round.formula);

                // Find the last round for the current shape
                const roundsForCurrentShape = this.rounds.filter(round => round.shape === this.round.shape);

                const lastRound = roundsForCurrentShape[roundsForCurrentShape.length - 1];

                // If there is a last round for the current shape, compare the validated value to its result
                if (lastRound && validatedValue !== lastRound.result) {
                    this.warningMessage = `The current validated value (${validatedValue}) does not match the last result for this shape (${lastRound.result}).`;
                    this.lastResultMessage = `Last result: ${lastRound.result}`;
                    // You might want to stop the form submission or handle it differently here
                } else {
                    this.warningMessage = '';
                    this.lastResultMessage = `Last result: N/A`;
                }

                // Validate and calculate result only if there's user input
                const isValidFormula = this.calculateFormula(this.round.formula);
                this.isFormulaValid = isValidFormula;
                if (isValidFormula) {
                    this.round.result = this.calculateResult(this.round.formula);
                    this.currentResultMessage = `Current Result: ${this.currentResult}`;
                    this.validatedValueMessage = `Validated Value: ${this.calculateValidatedValue(this.round.formula)}`;
                }
            } else {
                // Reset currentResultMessage if there's no user input
                this.currentResultMessage = 'Current Result: 0';
                this.validatedValueMessage = 'Validated Value: 0';
            }
        },
        
        formatUserInput() {
            // Remove spaces from the formula input
            this.round.formula = this.round.formula.replace(/\s/g, '');
            this.round.formula = this.round.formula.replace(/^,/g, '');
            this.round.formula = this.round.formula.replace(/,,/g, ',');
            //this.round.formula = this.round.formula.replace(/,/g, ', ');
            this.round.formula = this.round.formula.toLowerCase();
        },

        calculateResult(formula) {
            const parts = formula.split(',').map(part => part.trim());
            let result = 0;
            parts.forEach(part => {
                if (part === 'sc' || part === 'dec' || part === 'slst' || part === 'ch') {
                    result += 1;
                } else if (part === 'inc') {
                    result += 2;
                } else if (part === 'tinc') {
                    result += 3;
                } else {
                    const number = parseInt(part);
                    if (!isNaN(number)) {
                        result += number;
                    }
                }
            });
            return result;
        },

        async createRound() {
            try {
                
                if (this.round.formula.endsWith(',')) {
                    this.round.formula = this.round.formula.slice(0, -1);
                }

                if (this.round.formula && this.round.formula.trim() === '') {
                    this.currentResultMessage = 'Formula cannot be empty';
                    return;
                }

                if (!this.validateFormData()) {
                    // Data is not valid, so return without submitting
                    return;
                }
                
                const { isValid, currentResult } = await this.calculateFormula(this.round.formula);

                if (!isValid) {
                    // If the formula is invalid, do not proceed
                    this.currentResultMessage = 'Invalid formula';
                    return;
                }
                // Calculate the result based on the formula
                //const result = this.calculateResult(this.round.formula);
                
                // Send the request to create the round
                const response = await fetch('http://127.0.0.1:8000/track/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        formula: this.round.formula,
                        result: currentResult,
                        comment:this.round.comment,
                        shape: this.round.shape
                    })
                });

                // Check if the request was successful
                if (!response.ok) {
                    throw new Error('Failed to create round');
                }

                // Refresh the rounds data
                await this.getRounds();
                await this.resetValues();
            } catch (error) {
                console.error('Error creating round:', error);
            }
        },
        
        async editRound() {
            try {
                //const result = this.calculateResult(this.round.formula);
                //this.round.result = result;

                const { isValid, currentResult } = await this.calculateFormula(this.round.formula);

                if (!isValid) {
                    // If the formula is invalid, do not proceed
                    this.warningMessage = 'Invalid formula';
                    return;
                }
                const response = await fetch(`http://127.0.0.1:8000/track/${this.round.id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        formula: this.round.formula, 
                        result: currentResult, 
                        comment:this.round.comment })
                });
                if (!response.ok) {
                    throw new Error('Failed to update round');
                }
                await this.getRounds();
                await this.resetValues();
            } catch (error) {
                console.error('Error updating round:', error);
            }
        },

        async deleteRound(round) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/track/${round.id}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to delete round');
                }
                await this.getRounds();
                await this.resetValues();
            } catch (error) {
                console.error('Error deleting round:', error);
            }
        },

        async fetchPattern() {
            try {
                const response = await fetch('http://127.0.0.1:8000/pattern/');
                if (!response.ok) {
                    throw new Error('Failed to fetch pattern data');
                }
                const data = await response.json();
                this.pattern = data.pattern;
                console.log('Pattern:', this.pattern);
            } catch (error) {
                console.error('Error fetching pattern:', error);
            }
        },

        async resetValues() {
            this.round = {};
            this.currentResultMessage = '';
            this.validatedValueMessage = '';
            this.lastResultMessage = '';
            this.warningMessage = '';
        },
        toggleAccordion(shapeId) {
            this.openShapeId = this.openShapeId === shapeId ? null : shapeId;
        },
        isShapeOpen(shapeId) {
            return this.openShapeId === shapeId;
        },
    }
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    transition: 0.3s ease;
}
</style>
