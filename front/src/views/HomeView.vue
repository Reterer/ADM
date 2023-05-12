<template>
  <div>
    <h2>Здесь будет какой-то поиск</h2>
    <p>Message is: {{ search_text }}</p>
    <form @submit.prevent="submit">
      <input type="text" v-model="search_text">
      <button type="submit">
        Submit From Vue Property
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      search_text: "",
    }
  },
  methods: {
    submit() {
      axios.post('/api', { name: this.name })
        .then(res => {
          // do something with res
        })
        .catch(err => {/* catch error */ });
    }
  }
}

</script>