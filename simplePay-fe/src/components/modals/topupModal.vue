<template>
  <dialog id="topupModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Ricarica conto</h2>
        <button class="btn btn-sm btn-circle" onclick="topupModal.close()">✕</button>
      </div>

      <form @submit.prevent="topupMoney">
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo da ricaricare</span>
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
            <span class="label-text font-medium">Numero carta</span>
          </label>
          <input
            type="tel"
            pattern="[0-9\s]{13,19}"
            v-model="form.card_number"
            class="input input-bordered w-full"
            placeholder="1234 5678 9012 3456"
            maxlength="16"
            required
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Intestatario carta</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Nome Cognome"
            v-model="form.card_holder"
            required
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text font-medium">Data scadenza</span>
            </label>
            <div class="flex items-center">
              <input
                type="text"
                class="input input-bordered w-1/2"
                placeholder="MM"
                maxlength="2"
                v-model="form.expiry_month"
                max="12"
                required
              />
              <span class="mx-1">/</span>
              <input
                type="text"
                class="input input-bordered w-1/2"
                placeholder="AA"
                maxlength="2"
                v-model="form.expiry_year"
                required
              />
            </div>
          </div>

          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text font-medium">CVV</span>
            </label>
            <input
              type="text"
              class="input input-bordered w-full"
              placeholder="123"
              maxlength="3"
              v-model="form.cvv"
              required
            />
          </div>
        </div>

        <button type="submit" class="btn bg-black text-white w-full">Ricarica</button>
        <button type="button" class="btn w-full mt-4" onclick="topupModal.close()">Annulla</button>
      </form>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import type { DepositRequest } from '@/api/wallet'
import wallet from '@/api/wallet'
import { ref } from 'vue'

const form = ref<DepositRequest>({
  amount: 0,
  card_number: '',
  card_holder: '',
  expiry_month: 0,
  expiry_year: 0,
  cvv: ''
})

const topupMoney = async () => {
  try {
    await wallet.deposit(form.value!)
  } catch (error) {
    console.error('Error during top-up:', error)
  }
}
</script>
