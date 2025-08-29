<template>
  <div class="container mx-auto p-6s">
    <!-- Header -->
    <header class="flex justify-between items-center py-8 border-b border-base-300 mb-8">
      <div class="text-2xl font-semibold">Simple Pay</div>
      <div class="flex items-center gap-2">
        <div class="text-base">Mario Rossi</div>
        <button class="btn btn-ghost btn-sm px-2" @click="handleLogout" title="Logout">
          <span class="text-base text-sm">Logout</span>
        </button>
      </div>
    </header>

    <!-- Balance Section -->
    <section class="text-center mb-12">
      <div class="text-sm text-base-content/70 mb-2">Saldo disponibile</div>
      <div class="text-5xl font-light text-base-content">
        2.543<span class="text-base-content/70">,21 €</span>
      </div>
    </section>

    <!-- Actions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="openModal('sendModal')"
      >
        <span class="text-3xl mb-4 block">↗</span>
        <div class="font-medium mb-2">Invia</div>
        <div class="text-sm text-base-content/70">Invia denaro</div>
      </div>

      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="openModal('topupModal')"
      >
        <span class="text-3xl mb-4 block">+</span>
        <div class="font-medium mb-2">Ricarica</div>
        <div class="text-sm text-base-content/70">Aggiungi fondi</div>
      </div>

      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="openModal('transferModal')"
      >
        <span class="text-3xl mb-4 block">→</span>
        <div class="font-medium mb-2">Bonifico</div>
        <div class="text-sm text-base-content/70">Trasferimento bancario</div>
      </div>
    </div>

    <!-- Transaction History -->
    <section class="card bg-base-100 border border-base-300 p-6">
      <h2 class="text-lg font-medium mb-6 text-base-content">Transazioni recenti</h2>

      <div class="flex justify-between items-center py-4 border-b border-base-200">
        <div class="flex items-center">
          <div
            class="w-10 h-10 rounded-full bg-base-200 flex items-center justify-center mr-4 text-base-content/70"
          >
            ↙
          </div>
          <div>
            <h4 class="text-sm font-medium mb-1">Da Giulia Bianchi</h4>
            <p class="text-xs text-base-content/70">Oggi, 14:32</p>
          </div>
        </div>
        <div class="text-sm font-medium text-success">+150,00 €</div>
      </div>

      <div class="flex justify-between items-center py-4 border-b border-base-200">
        <div class="flex items-center">
          <div
            class="w-10 h-10 rounded-full bg-base-200 flex items-center justify-center mr-4 text-base-content/70"
          >
            ↗
          </div>
          <div>
            <h4 class="text-sm font-medium mb-1">A Marco Verdi</h4>
            <p class="text-xs text-base-content/70">Ieri, 19:45</p>
          </div>
        </div>
        <div class="text-sm font-medium text-error">-75,50 €</div>
      </div>

      <div class="flex justify-between items-center py-4">
        <div class="flex items-center">
          <div
            class="w-10 h-10 rounded-full bg-base-200 flex items-center justify-center mr-4 text-base-content/70"
          >
            +
          </div>
          <div>
            <h4 class="text-sm font-medium mb-1">Ricarica carta</h4>
            <p class="text-xs text-base-content/70">2 giorni fa</p>
          </div>
        </div>
        <div class="text-sm font-medium text-success">+500,00 €</div>
      </div>
    </section>
  </div>

  <!-- Send Money Modal -->
  <div id="sendModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Invia denaro</h2>
        <button class="btn btn-sm btn-circle" onclick="closeModal('sendModal')">✕</button>
      </div>

      <form>
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

        <button type="submit" class="btn btn-primary w-full">Invia</button>
        <button type="button" class="btn w-full mt-4" onclick="closeModal('sendModal')">
          Annulla
        </button>
      </form>
    </div>
  </div>

  <!-- Remaining modals converted to DaisyUI -->
  <!-- Receive Money Modal -->
  <div id="receiveModal" class="modal">
    <div class="modal-box">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-medium">Richiedi denaro</h2>
        <button class="btn btn-sm btn-circle" onclick="closeModal('receiveModal')">✕</button>
      </div>

      <form>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Da</span>
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
            <span class="label-text font-medium">Motivo</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Descrizione della richiesta"
          />
        </div>

        <button type="submit" class="btn btn-primary w-full">Invia richiesta</button>
        <button type="button" class="btn w-full mt-4" onclick="closeModal('receiveModal')">
          Annulla
        </button>
      </form>
    </div>
  </div>

  <!-- Additional modals follow the same pattern -->
  <!-- Remember to include daisyUI in your project setup -->
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, onUnmounted } from 'vue'

const router = useRouter()
const handleLogout = () => {
  localStorage.removeItem('userToken')
  localStorage.removeItem('userEmail')
  localStorage.removeItem('userName')
  router.push('/login')
}

// Funzione per aprire una modale
function openModal(modalId: string) {
  const modal = document.getElementById(modalId)
  if (modal) {
    modal.classList.add('active')
    document.body.style.overflow = 'hidden'
  }
}

// Funzione per chiudere una modale
function closeModal(modalId: string) {
  const modal = document.getElementById(modalId)
  if (modal) {
    modal.classList.remove('active')
    document.body.style.overflow = 'auto'
  }
}

// Funzione per mostrare un tab (se usato)
function showTab(tabId: string, event: Event) {
  const tabs = document.querySelectorAll('.tab')
  const tabContents = document.querySelectorAll('.tab-content')
  tabs.forEach((tab) => tab.classList.remove('active'))
  tabContents.forEach((content) => content.classList.remove('active'))
  if (event.target instanceof HTMLElement) {
    event.target.classList.add('active')
  }
  const tab = document.getElementById(tabId)
  if (tab) tab.classList.add('active')
}

// Listener per chiudere la modale cliccando fuori
function handleWindowClick(event: MouseEvent) {
  if (event.target instanceof HTMLElement && event.target.classList.contains('modal')) {
    event.target.classList.remove('active')
    document.body.style.overflow = 'auto'
  }
}

// Formatter per numero carta e data scadenza
function handleInputFormat(e: Event) {
  const target = e.target as HTMLInputElement
  if (!target) return
  if (target.placeholder === '1234 5678 9012 3456') {
    let value = target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '')
    let formattedValue = value.match(/.{1,4}/g)?.join(' ')
    target.value = formattedValue || value
  }
  if (target.placeholder === 'MM/AA') {
    let value = target.value.replace(/\D/g, '')
    if (value.length >= 2) {
      value = value.substring(0, 2) + '/' + value.substring(2, 4)
    }
    target.value = value
  }
}

onMounted(() => {
  window.addEventListener('click', handleWindowClick)
  document.addEventListener('input', handleInputFormat)
})

onUnmounted(() => {
  window.removeEventListener('click', handleWindowClick)
  document.removeEventListener('input', handleInputFormat)
})
</script>
