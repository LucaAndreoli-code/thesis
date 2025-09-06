/// <reference types="cypress" />
// ***********************************************
// This example commands.ts shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
//
export {}
declare global {
  namespace Cypress {
    interface Chainable {
      login(): void
    }
  }
}

export const baseUrl = 'http://0.0.0.0:8000/api/v1'

Cypress.Commands.add('login', () => {
  cy.request({
    method: 'POST',
    url: `${baseUrl}/auth/login`,
    body: {
      email: 'test@example.com', // o email, dipende dalla tua API
      password: 'password123'
    }
  }).then((response) => {
    // Salva il token nel localStorage
    window.localStorage.setItem('userToken', response.body.access_token)
  })
})
