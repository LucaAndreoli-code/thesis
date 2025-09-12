<template>
  <div id="app">
    <Alert />
    <router-view></router-view>
  </div>
</template>

<script>
import Alert from './components/alert/Alert.vue'

export default {
  name: 'App',
  components: {
    Alert
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
