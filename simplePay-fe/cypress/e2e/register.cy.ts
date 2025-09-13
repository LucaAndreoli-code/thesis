import { baseUrl } from '../support/commands'

const registerEndpoint = `${baseUrl}/auth/register`

describe('Register Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4173/register')
  })

  it('should display registration form correctly', () => {
    cy.contains('Simple Pay').should('be.visible')
    cy.contains('Registrazione').should('be.visible')

    cy.get('input[placeholder="Nome"]').should('be.visible')
    cy.get('input[placeholder="Cognome"]').should('be.visible')
    cy.get('input[placeholder="Email"]').should('be.visible')
    cy.get('input[placeholder="Password"]').should('be.visible')
    cy.get('input[placeholder="Conferma Password"]').should('be.visible')

    cy.get('button[type="submit"]').should('be.visible').and('contain', 'Registrati')

    cy.contains('Hai già un account?').should('be.visible')
    cy.get('a[href="/login"]').should('be.visible').and('contain', 'Accedi qui')
  })

  it('should show validation errors for empty form', () => {
    cy.get('button[type="submit"]').click()

    cy.get('input[placeholder="Nome"]:invalid').should('exist')
    cy.get('input[placeholder="Cognome"]:invalid').should('exist')
    cy.get('input[placeholder="Email"]:invalid').should('exist')
    cy.get('input[placeholder="Password"]:invalid').should('exist')
    cy.get('input[placeholder="Conferma Password"]:invalid').should('exist')
  })

  it('should show validation error for invalid email format', () => {
    cy.get('input[placeholder="Nome"]').type('Alberto')
    cy.get('input[placeholder="Cognome"]').type('Rossi')
    cy.get('input[placeholder="Email"]').type('invalid-email')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Conferma Password"]').type('password123')
    cy.get('button[type="submit"]').click()

    cy.get('input[placeholder="Email"]:invalid').should('exist')
  })

  it('should show alert when passwords do not match', () => {
    cy.get('input[placeholder="Nome"]').type('Mario')
    cy.get('input[placeholder="Cognome"]').type('Rossi')
    cy.get('input[placeholder="Email"]').type('mario@example.com')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Conferma Password"]').type('differentpassword')

    cy.get('button[type="submit"]').click()

    cy.get('#error-alert').should('be.visible').and('contain', 'Le password non coincidono')
  })

  it('should successfully register with valid data and clear register page data', () => {
    cy.intercept('POST', registerEndpoint).as('registerRequest')

    const uuid = crypto.randomUUID()

    cy.get('input[placeholder="Nome"]').type(uuid)
    cy.get('input[placeholder="Cognome"]').type('Rossi')
    cy.get('input[placeholder="Email"]').type(`${uuid}@example.com`)
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Conferma Password"]').type('password123')

    cy.get('button[type="submit"]').click()

    cy.wait('@registerRequest').then((interception) => {
      expect(interception.response?.body).to.deep.include({
        email: `${uuid}@example.com`,
        username: `${uuid}_rossi`,
        first_name: uuid,
        last_name: 'Rossi'
      })
      expect(interception.response?.statusCode).to.equal(200)
    })

    cy.get('a[href="/register"]').should('be.visible').click()
    cy.get('input[placeholder="Nome"]').should('have.value', '')
    cy.get('input[placeholder="Cognome"]').should('have.value', '')
    cy.get('input[placeholder="Email"]').should('have.value', '')
  })

  it('should handle registration error', () => {
    cy.intercept('POST', registerEndpoint, {
      statusCode: 400,
      body: { detail: 'User already exists' }
    }).as('registerError')

    cy.get('input[placeholder="Nome"]').type('Alberto')
    cy.get('input[placeholder="Cognome"]').type('Rossi')
    cy.get('input[placeholder="Email"]').type('existing@example.com')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Conferma Password"]').type('password123')

    cy.get('button[type="submit"]').click()

    cy.wait('@registerError')
  })

  it('should navigate to login page when clicking login link', () => {
    cy.get('a[href="/login"]').click()
    cy.url().should('include', '/login')
    cy.contains('Login').should('be.visible')
  })

  it('should have proper accessibility attributes', () => {
    cy.get('input[placeholder="Password"]').should('have.attr', 'autocomplete', 'new-password')
    cy.get('input[placeholder="Conferma Password"]').should(
      'have.attr',
      'autocomplete',
      'new-password'
    )

    cy.get('input[placeholder="Nome"]').should('have.attr', 'required')
    cy.get('input[placeholder="Cognome"]').should('have.attr', 'required')
    cy.get('input[placeholder="Email"]').should('have.attr', 'required')
    cy.get('input[placeholder="Password"]').should('have.attr', 'required')
    cy.get('input[placeholder="Conferma Password"]').should('have.attr', 'required')
  })
})
