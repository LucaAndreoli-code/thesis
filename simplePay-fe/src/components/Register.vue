<template>
  <div class="min-h-screen flex flex-col items-center justify-center">
    <h1 class="text-4xl font-bold mb-8 text-black">Simple Pay</h1>
    <div class="w-96 p-8 card bg-base-100 border border-base-300 shadow-md p-6 text-center">
      <h2 class="text-2xl font-light text-center mb-8 text-black">Registrazione</h2>

      <form @submit.prevent="withLoading(handleRegister)" class="space-y-6">
        <div>
          <input
            type="text"
            v-model="form.first_name"
            placeholder="Nome"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <div>
          <input
            type="text"
            v-model="form.last_name"
            placeholder="Cognome"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <div>
          <input
            type="email"
            v-model="form.email"
            placeholder="Email"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
          />
        </div>

        <div>
          <input
            type="password"
            v-model="form.password"
            placeholder="Password"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
            autocomplete="new-password"
          />
        </div>

        <div>
          <input
            type="password"
            v-model="form.confirmPassword"
            placeholder="Conferma Password"
            class="w-full p-3 border-b border-gray-300 bg-transparent focus:border-black focus:outline-none text-black"
            required
            autocomplete="new-password"
          />
        </div>

        <button
          :disabled="isLoading"
          type="submit"
          class="btn bg-black text-white w-full hover:bg-gray-800"
        >
          <span class="loading loading-dots" v-if="isLoading"></span>
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
import auth from '@/api/auth'
import { notify } from '@/service/alert'
import { isLoading, withLoading } from '@/service/loading'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    notify('error', 'Le password non coincidono!')
    return
  }

  try {
    await auth.register(
      form.value.first_name,
      form.value.last_name,
      form.value.email,
      form.value.password
    )
    router.push('/login')
  } catch (error) {
    console.error('Registration failed:', error)
  }
}
</script>
