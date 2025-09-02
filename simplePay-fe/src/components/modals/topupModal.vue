<template>
  <dialog id="topupModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Ricarica conto</h2>
        <button class="btn btn-sm btn-circle" onclick="topupModal.close()">✕</button>
      </div>

      <form>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo da ricaricare</span>
          </label>
          <input type="number" class="input input-bordered w-full" placeholder="0,00" step="0.01" />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Numero carta</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="1234 5678 9012 3456"
            maxlength="19"
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Intestatario carta</span>
          </label>
          <input type="text" class="input input-bordered w-full" placeholder="Nome Cognome" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text font-medium">Data scadenza</span>
            </label>
            <input
              type="text"
              class="input input-bordered w-full"
              placeholder="MM/AA"
              maxlength="5"
            />
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
            />
          </div>
        </div>

        <button class="btn bg-black text-white w-full">Ricarica</button>
        <button type="button" class="btn w-full mt-4" onclick="topupModal.close()">
          Annulla
        </button>
      </form>
    </div>
  </dialog>
</template>
