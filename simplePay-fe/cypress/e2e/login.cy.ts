import { baseUrl } from '../support/commands'

const loginEndpoint = `${baseUrl}/auth/login`

describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/login')
  })

  it('should display login form correctly', () => {
    cy.contains('Simple Pay').should('be.visible')
    cy.contains('Login').should('be.visible')

    cy.get('input[type="email"]').should('be.visible').and('have.attr', 'placeholder', 'Email')
    cy.get('input[type="password"]')
      .should('be.visible')
      .and('have.attr', 'placeholder', 'Password')

    cy.get('button[type="submit"]').should('be.visible').and('contain', 'Accedi')

    cy.contains('Non hai un account?').should('be.visible')
    cy.get('a[href="/register"]').should('be.visible').and('contain', 'Registrati qui')
  })

  it('should show validation errors for empty form', () => {
    cy.get('button[type="submit"]').click()

    cy.get('input[type="email"]:invalid').should('exist')
    cy.get('input[type="password"]:invalid').should('exist')
  })

  it('should show validation error for invalid email format', () => {
    cy.get('input[type="email"]').type('invalid-email')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    cy.get('input[type="email"]:invalid').should('exist')
  })

  it('should attempt login with valid credentials', () => {
    cy.intercept('POST', loginEndpoint).as('loginRequest')

    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')

    cy.get('button[type="submit"]').click()

    cy.wait('@loginRequest').then((interception) => {
      expect(interception.request.body).to.deep.equal({
        email: 'test@example.com',
        password: 'password123'
      })
    })
  })

  it('should handle login error', () => {
    cy.intercept('POST', loginEndpoint).as('loginError')

    cy.get('input[type="email"]').type('wrong@example.com')
    cy.get('input[type="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()

    cy.wait('@loginError')
  })

  it('should show loading state during login', () => {
    cy.intercept('POST', loginEndpoint).as('loginDelay')

    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    cy.get('.loading-dots').should('be.visible')
    cy.get('button[type="submit"]').should('be.disabled')

    cy.wait('@loginDelay')
  })

  it('should have proper accessibility attributes', () => {
    cy.get('input[type="email"]').should('have.attr', 'autocomplete', 'email')
    cy.get('input[type="password"]').should('have.attr', 'autocomplete', 'current-password')

    cy.get('input[type="email"]').should('have.attr', 'required')
    cy.get('input[type="password"]').should('have.attr', 'required')
  })
})
