<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="w-96 p-8 card bg-base-100 border border-base-300 shadow-md p-6 text-center">
      <h2 class="text-2xl font-light text-center mb-8 text-black">Registrazione</h2>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <input
            type="text"
            v-model="name"
            placeholder="Nome completo"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

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

        <div>
          <input
            type="password"
            v-model="confirmPassword"
            placeholder="Conferma Password"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <button type="submit" class="w-full mt-8 py-3 bg-black text-white hover:bg-gray-800">
          Registrati
        </button>
      </form>

      <p class="text-center mt-8 text-sm text-gray-600">
        Hai già un account?
        <router-link to="/login" class="text-black underline"> Accedi qui </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleRegister = () => {
  if (password.value !== confirmPassword.value) {
    alert('Le password non coincidono!')
    return
  }

  console.log('Register:', { name: name.value, email: email.value })

  if (email.value && password.value) {
    localStorage.setItem('userToken', 'fake-jwt-token')
    localStorage.setItem('userEmail', email.value)
    localStorage.setItem('userName', name.value)
    router.push('/home')
  }
}
</script>
