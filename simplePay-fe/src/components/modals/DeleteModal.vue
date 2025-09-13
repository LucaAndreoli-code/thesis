<template>
  <dialog id="deleteModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Eliminazione account</h2>
        <button type="button" class="btn btn-sm btn-circle" onclick="deleteModal.close()">✕</button>
      </div>

      <div class="grid gap-4">
        <p class="text-base-content/70 mb-4">
          Sei sicuro di voler eliminare il tuo account? Questa azione è irreversibile e comporterà
          la perdita di tutti i tuoi dati, incluse le transazioni e il saldo attuale.
        </p>
      </div>
      <button
        id="deleteSubmit"
        :disabled="isLoading"
        :onclick="confirmDelete"
        class="btn bg-black text-white w-full hover:bg-gray-800"
      >
        <span class="loading loading-dots" v-if="isLoading"></span>Elimina
      </button>
      <button type="button" class="btn w-full mt-6" onclick="deleteModal.close()">Chiudi</button>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import user from '@/api/user'
import { notify } from '@/service/alert'
import { isLoading } from '@/service/loading'
import { useRouter } from 'vue-router'

const router = useRouter()

const confirmDelete = async () => {
  isLoading.value = true
  try {
    await user.deleteAccount()
    const deleteModal = document.getElementById('deleteModal') as HTMLDialogElement
    deleteModal.close()
    localStorage.removeItem('userToken')
    notify('success', 'Account eliminato con successo.')
    await router.push('/login')
  } catch (error) {
    console.error("Errore durante l'eliminazione dell'account:", error)
  } finally {
    isLoading.value = false
  }
}
</script>
