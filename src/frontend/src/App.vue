<template>
  <div id="app">

<form @submit.prevent="submitForm">
  <div class="form-group row">
    <input type="text" class="form-control col-3 mx-2" placeholder="Name" v-model="project.name">
    <button class="btn btn-success">Submit</button>
  </div>
</form>

    <table class="table">
      <thead>
        <th>Name</th>
        <th>Author</th>
        <th>Created</th>
        <th>Modified</th>
      </thead>
      <tbody>
        <tr v-for="project in projects" :key="project.id" @dblclick="$data.project=project">
          <td>{{ project.name }}</td>
          <td>{{ project.author }}</td>
          <td>{{ project.created }}</td>
          <td>{{ project.modified }}</td>
          <td>
            <button class="btn btn-outline-danger btn-sm mx-1" @click="deleteProject(project)">x</button>
          </td>
        </tr>
      </tbody>
    </table>
    
  </div>
</template>

<script>

export default {
  name: 'App',
  data(){
    return{
      projects: [],
      project: {},
    }
  },
  
  async created(){
    await this.getProjects();
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
