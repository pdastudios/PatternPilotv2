<template>
  <div id="app">

  <form @submit.prevent="submitForm">
    <div class="form-group row">
      <input type="text" class="form-control col-3 mx-2" placeholder="Formula" v-model="round.formula">
      <button class="btn btn-success">Submit</button>
    </div>
  </form>
  <div class="card">
    <table class="table">
      <thead>
        <th>Round</th>
        <th>Pattern</th>
        <th>Result</th>
      </thead>
      <tbody>
        <tr v-for="round in rounds" :key="round.id" @dblclick="$data.round=round">
          <td>{{ round.number }}</td>
          <td>{{ round.formula }}</td>
          <td>{{ round.result }}</td>
          <td>
            <button class="btn btn-outline-danger btn-sm mx-1" @click="deleteProject(project)">x</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </div>
</template>

<script>

export default {
  name: 'PatternCalc',
  data(){
    return{
      rounds: [],
      round: {},
      pattern:''
    }
  },
  
  async created(){ // When the 
    await this.getProjects();
    await this.fetchPattern();
  },

  methods: {
    submitForm(){
      if ( this.project.id === undefined ){
        this.createProject();
      } else {
        this.editProject();
      }
    },

    async getProjects(){
      var response = await fetch('http://127.0.0.1:8000/tracker/')
      this.projects = await response.json();
    },

    async createProject(){
      await this.getProjects();

      await fetch('http://127.0.0.1:8000/tracker/', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.project)
      });
      console.log(this.project)
      await this.getProjects();
    },

    async editProject(){
      await this.getProjects();

      await fetch(`http://127.0.0.1:8000/tracker/${this.project.id}/`, {
        method: 'put',
        headers: {
          'Content-Type': 'application/json',

        },
        body: JSON.stringify(this.project)
      });

      await this.getProjects();
      this.project = {};
    },

    async deleteProject(project){
      await this.getProjects();
      console.log("this is PORJ3CE VAR" + project.id)
      await fetch(`http://127.0.0.1:8000/tracker/${project.id}/`, {
        method: 'delete',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.project)
      });

      await this.getProjects();
    },
    
    async fetchPattern() {
    try {
      const response = await fetch('http://127.0.0.1:8000/pattern/');
      if (!response.ok) {
        throw new Error('Failed to fetch pattern data');
      }
      const data = await response.json();
      this.pattern = data.pattern;
      console.log('Pattern:', this.pattern); // Log pattern data
    } catch (error) {
      console.error('Error fetching pattern:', error);
    }
  }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
