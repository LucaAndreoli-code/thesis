<template>
  <dialog id="sendModal" class="modal">
    <div class="modal-box">
      <form method="dialog" @submit.prevent="sendMoney">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-medium">Invia denaro</h2>
          <button type="button" class="btn btn-sm btn-circle" onclick="sendModal.close()">✕</button>
        </div>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Destinatario</span>
          </label>
          <input
            type="email"
            class="input input-bordered w-full"
            placeholder="Email, telefono o nome"
            required
            v-model="form.to_user_email"
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo</span>
          </label>
          <input
            type="number"
            class="input input-bordered w-full"
            placeholder="0,00"
            step="0.01"
            pattern="^\d+(\.\d{1,2})?$"
            v-model="form.amount"
            required
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Messaggio (opzionale)</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Aggiungi una nota"
            v-model="form.description"
          />
        </div>

        <button class="btn bg-black text-white w-full">Invia</button>
        <button type="button" class="btn w-full mt-4" onclick="sendModal.close()">Annulla</button>
      </form>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import type { SendMoneyRequest } from '@/api/payments'
import payments from '@/api/payments'
import { ref } from 'vue'

const form = ref<SendMoneyRequest>({
  amount: 0,
  to_user_email: '',
  description: ''
})

const sendMoney = async () => {
  try {
    payments.sendMoney(form.value)
  } catch (error) {
    console.error('Error sending money:', error)
  }
}
</script>
