<template>
  <dialog id="detailModal" class="modal">
    <div class="modal-box" v-if="transaction">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Dettagli transazione</h2>
        <button type="button" class="btn btn-sm btn-circle" onclick="detailModal.close()">✕</button>
      </div>

      <div class="grid gap-4">
        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Importo</span>
          <span>{{ transaction.amount }} {{ transaction.currency }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Descrizione</span>
          <span>{{ transaction.description || 'Nessuna descrizione' }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Valuta</span>
          <span>{{ transaction.currency }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Codice riferimento</span>
          <span>{{ transaction.reference_code }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Stato</span>
          <span>
            <span v-if="transaction.status === 'completed'" class="badge badge-success gap-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-4 h-4"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </span>
            <span v-else-if="transaction.status === 'canceled'" class="badge badge-error gap-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-4 h-4"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </span>
            <span v-else-if="transaction.status === 'pending'" class="badge badge-warning gap-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-4 h-4"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </span>
            <span v-else>{{ transaction.status }}</span>
          </span>
        </div>

        <div class="flex justify-between items-center py-2 border-b">
          <span class="font-medium">Data</span>
          <span>{{ new Date(transaction.created_at).toLocaleString('it-IT') }}</span>
        </div>
      </div>

      <button type="button" class="btn w-full mt-6" onclick="detailModal.close()">Chiudi</button>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import type { Transaction } from '@/api/payments'

defineProps<{
  transaction: Transaction
}>()
</script>
