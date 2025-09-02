<template>
  <dialog id="transferModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Bonifico bancario</h2>
        <button class="btn btn-sm btn-circle" onclick="transferModal.close()">✕</button>
      </div>

      <form @submit.prevent="withLoading(transferMoney)">
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
            maxlength="34"
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

        <button
          :disabled="isLoading"
          type="submit"
          class="btn bg-black text-white w-full hover:bg-gray-800"
        >
          <span class="loading loading-dots" v-if="isLoading"></span> Trasferisci
        </button>
        <button
          :disabled="isLoading"
          type="button"
          class="btn w-full mt-4"
          onclick="transferModal.close()"
        >
          Annulla
        </button>
      </form>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import wallet, { type WithdrawRequest } from '@/api/wallet'
import { notify } from '@/service/alert'
import { isLoading, withLoading } from '@/service/loading'
import { ref } from 'vue'

const emit = defineEmits(['refresh'])

const form = ref<WithdrawRequest>({
  amount: null,
  bank_account: '',
  back_account_name: ''
})

const transferMoney = async () => {
  try {
    await wallet.withdraw(form.value!)
    notify('success', 'Bonifico effettuato con successo!')
  } catch (error) {
    console.error(error)
  } finally {
    const transferModal = document.getElementById('transferModal') as HTMLDialogElement
    transferModal.close()
    clearForm()
  }
}

const clearForm = () => {
  emit('refresh')
  form.value = {
    amount: null,
    bank_account: '',
    back_account_name: ''
  }
}
</script>
