<template>
  <dialog id="sendModal" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-medium">Invia denaro</h2>
          <button class="btn btn-sm btn-circle">✕</button>
        </div>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Destinatario</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Email, telefono o nome"
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo</span>
          </label>
          <input type="number" class="input input-bordered w-full" placeholder="0,00" step="0.01" />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Messaggio (opzionale)</span>
          </label>
          <input type="text" class="input input-bordered w-full" placeholder="Aggiungi una nota" />
        </div>

        <button class="btn bg-black text-white w-full">Invia</button>
        <button class="btn w-full mt-4">Annulla</button>
      </form>
    </div>
  </dialog>
</template>
