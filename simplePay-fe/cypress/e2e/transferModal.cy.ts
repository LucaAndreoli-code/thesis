import { baseUrl } from '../support/commands'

const transferEndpoint = `${baseUrl}/wallet/withdraw`

describe('Transfer Modal', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('http://localhost:5173/home')

    cy.get('div').contains('Trasferimento bancario').click()

    cy.get('#transferModal').should('be.visible')
  })

  it('should display transfer modal correctly', () => {
    cy.contains('Trasferimento bancario').should('be.visible')
    cy.get('#closeTransferModal').should('be.visible')

    cy.get('#transferAmount').should('be.visible').and('have.attr', 'placeholder', '0,00')
    cy.get('#transferIban')
      .should('be.visible')
      .and('have.attr', 'placeholder', 'IT60X0542811101000000123456')
    cy.get('#transferAccountHolder')
      .should('be.visible')
      .and('have.attr', 'placeholder', 'Nome Cognome')

    cy.contains('Importo da trasferire').should('be.visible')
    cy.contains('IBAN').should('be.visible')
    cy.contains('Intestatario conto').should('be.visible')

    cy.get('#transferSubmit').should('be.visible').and('contain', 'Trasferisci')
    cy.get('#transferCancel').should('be.visible').and('contain', 'Annulla')
  })

  it('should show validation errors for empty required fields', () => {
    cy.get('#transferSubmit').click()

    cy.get('#transferAmount:invalid').should('exist')
    cy.get('#transferIban:invalid').should('exist')
    cy.get('#transferAccountHolder:invalid').should('exist')
  })

  it('should validate input field attributes', () => {
    cy.get('#transferAmount')
      .should('have.attr', 'type', 'number')
      .should('have.attr', 'step', '0.01')
      .should('have.attr', 'pattern', '^\\d+(\\.\\d{1,2})?$')
      .should('have.attr', 'required')

    cy.get('#transferIban')
      .should('have.attr', 'type', 'text')
      .should('have.attr', 'pattern', '[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}')
      .should('have.attr', 'maxlength', '34')
      .should('have.attr', 'required')

    cy.get('#transferAccountHolder')
      .should('have.attr', 'type', 'text')
      .should('have.attr', 'required')
  })

  it('should successfully transfer with valid data', () => {
    cy.intercept('POST', transferEndpoint).as('transferRequest')

    cy.get('#transferAmount').type('250.75')
    cy.get('#transferIban').type('IT60X0542811101000000111111')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()

    cy.wait('@transferRequest')

    cy.get('#transferModal').should('not.be.visible')

    cy.contains('Bonifico effettuato con successo!').should('be.visible')
  })

  it('should handle minimum amount transfer', () => {
    cy.intercept('POST', transferEndpoint).as('minTransferRequest')

    cy.get('#transferAmount').type('0.01')
    cy.get('#transferIban').type('IT60X0542811101000000111111')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()
    cy.wait('@minTransferRequest')
  })

  it('should handle transfer error', () => {
    cy.intercept('POST', transferEndpoint, {
      statusCode: 400,
      body: { detail: 'Insufficient funds' }
    }).as('transferError')

    cy.get('#transferAmount').type('10000.00')
    cy.get('#transferIban').type('IT60X0542811101000000999999')
    cy.get('#transferAccountHolder').type('Invalid Account')

    cy.get('#transferSubmit').click()

    cy.wait('@transferError')

    cy.get('#transferModal').should('not.be.visible')
  })

  it('should show loading state during transfer', () => {
    cy.intercept('POST', transferEndpoint, {
      delay: 1000
    }).as('transferDelay')

    cy.get('#transferAmount').type('100.00')
    cy.get('#transferIban').type('IT60X0542811101000000111111')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()

    cy.get('#transferSubmit').should('be.disabled')
    cy.get('#transferCancel').should('be.disabled')

    cy.wait('@transferDelay')
  })

  it('should close modal when clicking X button', () => {
    cy.get('#closeTransferModal').click()
    cy.get('#transferModal').should('not.be.visible')
  })

  it('should close modal when clicking Cancel button', () => {
    cy.get('#transferCancel').click()
    cy.get('#transferModal').should('not.be.visible')
  })

  it('should clear form after successful transfer', () => {
    cy.intercept('POST', transferEndpoint).as('transferSuccess')

    cy.get('#transferAmount').type('150.00')
    cy.get('#transferIban').type('IT60X0542811101000000111111')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()
    cy.wait('@transferSuccess')

    cy.get('div').contains('Trasferimento bancario').click()

    cy.get('#transferAmount').should('have.value', '')
    cy.get('#transferIban').should('have.value', '')
    cy.get('#transferAccountHolder').should('have.value', '')
  })

  it('should validate IBAN format', () => {
    cy.get('#transferIban').type('INVALIDIBAN')
    cy.get('#transferAmount').type('100.00')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()

    cy.get('#transferIban:invalid').should('exist')
  })

  it('should validate IBAN length', () => {
    cy.get('#transferIban').type('IT60X0542811101000000111111TOOLONGFORIBAN')
    cy.get('#transferIban').should('have.value', 'IT60X0542811101000000111111TOOLONG')
  })

  it('should handle decimal amounts correctly', () => {
    cy.intercept('POST', transferEndpoint).as('decimalTransferRequest')

    cy.get('#transferAmount').type('123.45')
    cy.get('#transferIban').type('IT60X0542811101000000111111')
    cy.get('#transferAccountHolder').type('Mario Rossi')

    cy.get('#transferSubmit').click()
    cy.wait('@decimalTransferRequest')
  })
})
