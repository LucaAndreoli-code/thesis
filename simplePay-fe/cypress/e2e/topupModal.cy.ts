import { baseUrl } from '../support/commands'

const depositEndpoint = `${baseUrl}/wallet/deposit`

describe('Topup Modal', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('http://localhost:5173/home')

    cy.get('div').contains('Aggiungi fondi').click()

    cy.get('#topupModal').should('be.visible')
  })

  it('should display topup modal correctly', () => {
    cy.contains('Ricarica conto').should('be.visible')
    cy.get('#closeTopupModal').should('be.visible')

    cy.get('#topupCardNumber')
      .should('be.visible')
      .and('have.attr', 'placeholder', '1234 5678 9012 3456')
    cy.get('#topupCardHolder').should('be.visible').and('have.attr', 'placeholder', 'Nome Cognome')
    cy.get('#topupCvv').should('be.visible').and('have.attr', 'placeholder', '123')

    cy.contains('Importo da ricaricare').should('be.visible')
    cy.contains('Numero carta').should('be.visible')
    cy.contains('Intestatario carta').should('be.visible')
    cy.contains('Data scadenza').should('be.visible')
    cy.contains('CVV').should('be.visible')

    cy.get('#topupSubmit').should('be.visible').and('contain', 'Ricarica')
    cy.get('#topupCancel').should('be.visible').and('contain', 'Annulla')
  })

  it('should show validation errors for empty required fields', () => {
    cy.get('#topupSubmit').click()

    cy.get('#toputAmount:invalid').should('exist')
    cy.get('#topupCardNumber:invalid').should('exist')
    cy.get('#topupCardHolder:invalid').should('exist')
    cy.get('#topupExpiryDate:invalid').should('exist')
    cy.get('#topupCvv:invalid').should('exist')
  })

  it('should validate input field attributes', () => {
    cy.get('#toputAmount')
      .should('have.attr', 'type', 'number')
      .should('have.attr', 'step', '0.01')
      .should('have.attr', 'pattern', '^\\d+(\\.\\d{1,2})?$')
      .should('have.attr', 'required')

    cy.get('#topupCardNumber')
      .should('have.attr', 'type', 'tel')
      .should('have.attr', 'pattern', '[0-9\\s]{13,19}')
      .should('have.attr', 'maxlength', '16')
      .should('have.attr', 'required')

    cy.get('#topupCvv').should('have.attr', 'maxlength', '3').should('have.attr', 'required')
  })

  it('should successfully topup with valid card data', () => {
    cy.intercept('POST', depositEndpoint).as('topupRequest')

    cy.get('#toputAmount').type('100.50')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()

    cy.wait('@topupRequest')

    cy.get('#topupModal').should('not.be.visible')

    cy.contains('Ricarica effettuata con successo!').should('be.visible')
  })

  it('should handle minimum amount topup', () => {
    cy.intercept('POST', depositEndpoint).as('minTopupRequest')

    cy.get('#toputAmount').type('0.01')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()
    cy.wait('@minTopupRequest')
  })

  it('should handle large amount topup', () => {
    cy.intercept('POST', depositEndpoint).as('largeTopupRequest')

    cy.get('#toputAmount').type('9999.99')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()
    cy.wait('@largeTopupRequest')
  })

  it('should handle topup error', () => {
    cy.intercept('POST', depositEndpoint, {
      statusCode: 400,
      body: { detail: 'Invalid card details' }
    }).as('topupError')

    cy.get('#toputAmount').type('50.00')
    cy.get('#topupCardNumber').type('4000000000000002')
    cy.get('#topupCardHolder').type('Invalid Card')
    cy.get('#topupExpiryDate').type('01')
    cy.get('#topupExpiryYear').type('20')
    cy.get('#topupCvv').type('000')

    cy.get('#topupSubmit').click()

    cy.wait('@topupError')

    cy.get('#topupModal').should('not.be.visible')
  })

  it('should show loading state during topup', () => {
    cy.intercept('POST', depositEndpoint, {
      delay: 1000
    }).as('topupDelay')

    cy.get('#toputAmount').type('25.00')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()

    cy.get('#topupSubmit').should('be.disabled')
    cy.get('#topupCancel').should('be.disabled')

    cy.wait('@topupDelay')
  })

  it('should close modal when clicking X button', () => {
    cy.get('#closeTopupModal').click()
    cy.get('#topupModal').should('not.be.visible')
  })

  it('should close modal when clicking Cancel button', () => {
    cy.get('#topupCancel').click()
    cy.get('#topupModal').should('not.be.visible')
  })

  it('should clear form after successful topup', () => {
    cy.intercept('POST', depositEndpoint).as('topupSuccess')

    cy.get('#toputAmount').type('75.25')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()
    cy.wait('@topupSuccess')

    cy.get('div').contains('Aggiungi fondi').click()

    cy.get('#toputAmount').should('have.value', '')
    cy.get('#topupCardNumber').should('have.value', '')
    cy.get('#topupCardHolder').should('have.value', '')
    cy.get('#topupExpiryDate').should('have.value', '')
    cy.get('#topupExpiryYear').should('have.value', '')
    cy.get('#topupCvv').should('have.value', '')
  })

  it('should validate expiry month maximum value', () => {
    cy.get('#topupExpiryDate').should('have.attr', 'max', '12')

    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryDate').should('have.value', '12')
  })

  it('should handle different card number formats', () => {
    cy.intercept('POST', depositEndpoint).as('cardFormatRequest')

    const cardNumbers = ['1234567890123', '1234567890123456', '12345678901234567']

    cardNumbers.forEach((cardNumber, index) => {
      if (index > 0) {
        cy.get('div').contains('Aggiungi fondi').click()
      }

      cy.get('#toputAmount').clear().type('10.00')
      cy.get('#topupCardNumber').clear().type(cardNumber)
      cy.get('#topupCardHolder').clear().type('Mario Rossi')
      cy.get('#topupExpiryDate').clear().type('12')
      cy.get('#topupExpiryYear').clear().type('25')
      cy.get('#topupCvv').clear().type('123')

      cy.get('#topupSubmit').click()
      cy.wait('@cardFormatRequest')
    })
  })

  it('should validate CVV length', () => {
    cy.get('#topupCvv').type('1234')
    cy.get('#topupCvv').should('have.value', '123')
  })

  it('should emit refresh event after successful topup', () => {
    cy.intercept('POST', depositEndpoint).as('topupRefresh')

    cy.get('#toputAmount').type('30.00')
    cy.get('#topupCardNumber').type('1234567890123456')
    cy.get('#topupCardHolder').type('Mario Rossi')
    cy.get('#topupExpiryDate').type('12')
    cy.get('#topupExpiryYear').type('25')
    cy.get('#topupCvv').type('123')

    cy.get('#topupSubmit').click()
    cy.wait('@topupRefresh')
  })
})
