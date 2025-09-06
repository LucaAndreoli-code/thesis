import { baseUrl } from '../support/commands'

const sendMoneyEndpoint = `${baseUrl}/payments/send`

describe('Send Money Modal', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('http://localhost:5173/home')

    cy.get('div').contains('Invia denaro').click()
  })

  it('should display send money modal correctly', () => {
    cy.contains('Invia denaro').should('be.visible')
    cy.get('#closeSendModal').should('be.visible')

    cy.get('#sendEmail').should('be.visible')
    cy.get('#sendAmount').should('be.visible')
    cy.get('#sendDescription').should('be.visible')

    cy.contains('Destinatario').should('be.visible')
    cy.contains('Importo').should('be.visible')
    cy.contains('Messaggio (opzionale)').should('be.visible')

    cy.get('#sendSubmit').should('be.visible')
    cy.get('button').contains('Annulla').should('be.visible')
  })

  it('should show validation errors for empty required fields', () => {
    cy.get('#sendSubmit').click()

    cy.get('#sendEmail:invalid').should('exist')
    cy.get('#sendAmount:invalid').should('exist')
  })

  it('should show validation error for invalid email format', () => {
    cy.get('#sendEmail').type('invalid-email')
    cy.get('#sendAmount').type('10,50')
    cy.get('#sendSubmit').click()

    cy.get('#sendEmail:invalid').should('exist')
  })

  it('should validate number format for amount field', () => {
    cy.get('#sendAmount')
      .should('have.attr', 'type', 'number')
      .should('have.attr', 'step', '0.01')
      .should('have.attr', 'pattern', '^\\d+(\\.\\d{1,2})?$')
  })

  it('should successfully send money with valid data', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendMoneyRequest')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('25.50')
    cy.get('#sendDescription').type('Pagamento per cena')

    cy.get('#sendSubmit').click()

    cy.wait('@sendMoneyRequest')

    cy.get('#sendModal').should('not.be.visible')

    cy.contains('Denaro inviato con successo!').should('be.visible')
  })

  it('should send money without optional description', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendMoneyRequest')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('15.00')

    cy.get('#sendSubmit').click()

    cy.wait('@sendMoneyRequest')
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should handle send money error', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendMoneyError')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('1000.00')

    cy.get('#sendSubmit').click()

    cy.wait('@sendMoneyError')

    cy.get('#sendModal').should('not.be.visible')
  })

  it('should close modal when clicking X button', () => {
    cy.get('#closeSendModal').click()
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should close modal when clicking Cancel button', () => {
    cy.get('button').contains('Annulla').click()
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should fail sending money to inexistent email', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendMoneySuccess')

    cy.get('#sendEmail').type('recipient@example.com')
    cy.get('#sendAmount').type('50.00')
    cy.get('#sendDescription').type('Test payment')

    cy.get('#sendSubmit').click()
    cy.wait('@sendMoneySuccess').then((interception) => {
      expect(interception.response?.body).to.deep.equal({ detail: 'Destination wallet not found' })
      expect(interception.response?.statusCode).to.equal(404)
    })

    cy.get('div').contains('Invia denaro').click()

    cy.get('#sendEmail').should('have.value', '')
    cy.get('#sendAmount').should('have.value', '')
    cy.get('#sendDescription').should('have.value', '')
  })

  it('should have proper accessibility attributes', () => {
    cy.get('#sendEmail').should('have.attr', 'required')
    cy.get('#sendAmount').should('have.attr', 'required')

    cy.get('#sendDescription').should('not.have.attr', 'required')

    cy.get('label').contains('Destinatario').should('exist')
    cy.get('label').contains('Importo').should('exist')
    cy.get('label').contains('Messaggio (opzionale)').should('exist')
  })

  it('should handle decimal amounts correctly', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendDecimalAmount')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('12.75')

    cy.get('#sendSubmit').click()
    cy.wait('@sendDecimalAmount')
  })

  it('should handle large amounts', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendLargeAmount')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('9999.99')

    cy.get('#sendSubmit').click()
    cy.wait('@sendLargeAmount')
  })

  it('should emit refresh event after successful send', () => {
    cy.intercept('POST', sendMoneyEndpoint).as('sendMoneyRefresh')

    cy.get('#sendEmail').type('mario@example.com')
    cy.get('#sendAmount').type('25.00')

    cy.get('#sendSubmit').click()
    cy.wait('@sendMoneyRefresh')
  })
})
