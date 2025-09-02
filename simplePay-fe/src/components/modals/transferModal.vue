<template>
  <dialog id="transferModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Bonifico bancario</h2>
        <button class="btn btn-sm btn-circle" onclick="transferModal.close()">✕</button>
      </div>

      <form @submit.prevent="transferMoney">
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo da trasferire</span>
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
            <span class="label-text font-medium">IBAN</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="IT60X0542811101000000123456"
            pattern="[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}"
            v-model="form.bank_account"
            required
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Intestatario conto</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Nome Cognome"
            v-model="form.back_account_name"
            required
          />
        </div>

        <button class="btn bg-black text-white w-full">Trasferisci</button>
        <button type="button" class="btn w-full mt-4" onclick="transferModal.close()">
          Annulla
        </button>
      </form>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import wallet, { type WithdrawRequest } from '@/api/wallet'
import { ref } from 'vue'

const form = ref<WithdrawRequest>({
  amount: 0,
  bank_account: '',
  back_account_name: ''
})

const transferMoney = async () => {
  try {
    await wallet.withdraw(form.value!)
  } catch (error) {
    console.error(error)
  }
}
</script>
