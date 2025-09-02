<template>
  <div class="container mx-auto p-6s">
    <!-- Header -->
    <header class="flex justify-between items-center py-8 border-b border-base-300 mb-8">
      <div class="text-2xl font-semibold">Simple Pay</div>
      <div class="flex items-center gap-2">
        <div class="">
          <div class="text-base text-right">{{ userInformation?.email }}</div>
          <div class="text-base text-sm text-right">{{ userInformation?.username }}</div>
        </div>
        <div class="h-8 w-px bg-base-300 mx-2"></div>
        <button class="btn btn-ghost btn-sm px-2" @click="handleLogout" title="Logout">
          <span class="text-base text-sm">Logout</span>
        </button>
      </div>
    </header>

    <!-- Balance Section -->
    <section class="text-center mb-12">
      <div class="text-sm text-base-content/70 mb-2">Saldo disponibile</div>
      <div class="text-5xl font-light text-base-content">
        {{ userBalance?.balance
        }}<span class="text-base-content/70">&nbsp;{{ userBalance?.currency }}</span>
      </div>
    </section>

    <!-- Actions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="sendModal.showModal()"
      >
        <span class="text-3xl mb-4 block">↗</span>
        <div class="font-medium mb-2">Invia</div>
        <div class="text-sm text-base-content/70">Invia denaro</div>
      </div>

      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="topupModal.showModal()"
      >
        <span class="text-3xl mb-4 block">+</span>
        <div class="font-medium mb-2">Ricarica</div>
        <div class="text-sm text-base-content/70">Aggiungi fondi</div>
      </div>

      <div
        class="card bg-base-100 border border-base-300 hover:border-base-content hover:shadow-md cursor-pointer p-6 text-center"
        onclick="transferModal.showModal()"
      >
        <span class="text-3xl mb-4 block">→</span>
        <div class="font-medium mb-2">Bonifico</div>
        <div class="text-sm text-base-content/70">Trasferimento bancario</div>
      </div>
    </div>

    <!-- Transaction History -->
    <section class="card bg-base-100 border border-base-300 p-6">
      <h2 class="text-lg font-medium mb-6 text-base-content">Transazioni recenti</h2>

      <div v-if="userTransactions && userTransactions.data?.length > 0">
        <div
          v-for="transaction in userTransactions.data"
          :key="transaction.id"
          class="flex justify-between items-center py-4 border-b border-base-200"
          :class="{
            'border-b-0':
              userTransactions.data.indexOf(transaction) === userTransactions.data.length - 1
          }"
        >
          <div class="flex items-center">
            <div
              class="w-10 h-10 rounded-full bg-base-200 flex items-center justify-center mr-4 text-base-content/70"
            >
              {{
                transaction.transaction_type === 'receive'
                  ? '↙'
                  : transaction.transaction_type === 'deposit'
                  ? '+'
                  : '↗'
              }}
            </div>
            <div>
              <h4 class="text-sm font-medium mb-1">{{ transaction.description }}</h4>
              <p class="text-xs text-base-content/70">
                {{ new Date(transaction.created_at).toLocaleString() }}
              </p>
            </div>
          </div>
          <div
            class="text-sm font-medium"
            :class="
              ['receive', 'deposit'].includes(transaction.transaction_type)
                ? 'text-success'
                : 'text-error'
            "
          >
            {{ ['receive', 'deposit'].includes(transaction.transaction_type) ? '+' : '-'
            }}{{ transaction.amount.toFixed(2) }} {{ transaction.currency }}
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center mt-6">
          <span class="text-sm text-base-content/70">
            Pagina {{ page }} di {{ userTransactions.total_pages || 1 }}
          </span>
          <div class="flex gap-2">
            <button
              class="btn btn-sm btn-outline"
              :disabled="page <= 1"
              @click="changePage(page - 1)"
            >
              Precedente
            </button>
            <button
              class="btn btn-sm btn-outline"
              :disabled="page >= (userTransactions.total_pages || 1)"
              @click="changePage(page + 1)"
            >
              Successiva
            </button>
          </div>
        </div>
      </div>
      <div v-else class="py-4 text-center text-base-content/70">
        Nessuna transazione disponibile
      </div>
    </section>
  </div>

  <SendModal id="sendModal" @refresh="getUserInformations" />
  <TopupModal id="topupModal" @refresh="getUserInformations" />
  <TransferModal id="transferModal" @refresh="getUserInformations" />
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, onUnmounted, ref } from 'vue'
import TransferModal from './modals/transferModal.vue'
import TopupModal from './modals/topupModal.vue'
import SendModal from './modals/sendModal.vue'
import { getTokenInfo, type TokenInformations } from '@/service/jwt'
import payments, { type Paginated, type Transaction } from '@/api/payments'
import wallet, { type Balance } from '@/api/wallet'

const router = useRouter()
const userTransactions = ref<Paginated<Transaction> | null>(null)
const userBalance = ref<Balance | null>(null)
const page = ref(1)
const pageSize = ref(10)

const userInformation = ref<TokenInformations | null>(null)
const handleLogout = async () => {
  localStorage.removeItem('userToken')
  await router.push('/login')
}

onMounted(() => {
  userInformation.value = getTokenInfo()
  getUserInformations()
})

const changePage = (newPage: number) => {
  if (newPage < 1) return
  page.value = newPage
  getUserTransactions()
}

const getUserBalance = async () => {
  try {
    userBalance.value = await wallet.getBalance()
  } catch (error) {
    console.error('Error fetching balance:', error)
  }
}

const getUserTransactions = async () => {
  try {
    userTransactions.value = await payments.getTransactions(page.value, pageSize.value)
  } catch (error) {
    console.error('Error fetching transactions:', error)
  }
}

const getUserInformations = () => {
  getUserTransactions()
  getUserBalance()
}
</script>

<style scoped>
/* Override responsive container max-widths */
.container {
  @media (width >= 96rem) {
    max-width: 80rem;
  }

  @media (width <= 38rem) {
    max-width: 25rem;
  }
}
</style>
