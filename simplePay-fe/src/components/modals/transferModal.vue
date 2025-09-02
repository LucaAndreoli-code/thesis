<template>
  <dialog id="transferModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Bonifico bancario</h2>
        <button class="btn btn-sm btn-circle" onclick="transferModal.close()">✕</button>
      </div>

      <form>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo da trasferire</span>
          </label>
          <input type="number" class="input input-bordered w-full" placeholder="0,00" step="0.01" />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">IBAN</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="IT60X0542811101000000123456"
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Intestatario conto</span>
          </label>
          <input type="text" class="input input-bordered w-full" placeholder="Nome Cognome" />
        </div>

        <button class="btn bg-black text-white w-full">Trasferisci</button>
        <button type="button" class="btn w-full mt-4" onclick="transferModal.close()">
          Annulla
        </button>
      </form>
    </div>
  </dialog>
</template>
