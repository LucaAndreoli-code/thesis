<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="w-96 p-8 card bg-base-100 border border-base-300 hover:shadow-md p-6 text-center">
      <h2 class="text-2xl font-light text-center mb-8 text-black">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <input
            type="email"
            v-model="email"
            placeholder="Email"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <div>
          <input
            type="password"
            v-model="password"
            placeholder="Password"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full mt-8 py-3 bg-black text-white cursor-pointer hover:bg-gray-800"
        >
          Accedi
        </button>
      </form>

      <p class="text-center mt-8 text-sm text-gray-600">
        Non hai un account?
        <router-link to="/register" class="text-black underline"> Registrati qui </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = () => {
  console.log('Login:', email.value, password.value)

  if (email.value && password.value) {
    localStorage.setItem('userToken', 'fake-jwt-token')
    localStorage.setItem('userEmail', email.value)
    router.push('/home')
  }
}
</script>
