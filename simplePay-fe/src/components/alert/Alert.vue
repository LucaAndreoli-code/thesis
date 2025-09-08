<template>
    <!-- Info Alert -->
    <div id="info-alert" role="alert" class="alert alert-pos shadow-lg alert-info" v-if="alert.message && alert.type === 'info'">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="h-6 w-6 shrink-0 stroke-current"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
        </svg>
        <span>{{ alert.message }}</span>
    </div>

    <!-- Success Alert -->
    <div id="success-alert" role="alert" class="alert alert-pos shadow-lg alert-success" v-else-if="alert.message && alert.type === 'success'">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="stroke-current shrink-0 h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
        </svg>
        <span>{{ alert.message }}</span>
    </div>

    <!-- Error Alert -->
    <div id="error-alert" role="alert" class="alert alert-pos shadow-lg alert-error" v-else-if="alert.message && alert.type === 'error'">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="stroke-current shrink-0 h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
        </svg>
        <span>{{ alert.message }}</span>
    </div>

    <!-- Default/Warning Alert -->
    <div id="warning-alert" role="alert" class="alert alert-pos shadow-lg alert-warning" v-else-if="alert.message">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="stroke-current shrink-0 h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
        </svg>
        <span>{{ alert.message }}</span>
    </div>
</template>

<script lang="ts" setup>
import { alert } from '@/service/alert'
</script>

<style scoped>
.alert-pos {
  position: absolute;
  top: 1rem;
  right: 1rem;
  margin: 0.5rem;
  z-index: 1000;
}
</style>
