describe('Send Money Modal', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('http://localhost:5173/home')

    cy.get('div').contains('Invia denaro').click()
  })

  it('should display send money modal correctly', () => {
    cy.contains('Invia denaro').should('be.visible')
    cy.get('button[onclick="sendModal.close()"]').should('be.visible')

    cy.get('input[id="emailInput"]').should('be.visible')
    cy.get('input[id="amountInput"]').should('be.visible')
    cy.get('input[placeholder="Aggiungi una nota"]').should('be.visible')

    cy.contains('Destinatario').should('be.visible')
    cy.contains('Importo').should('be.visible')
    cy.contains('Messaggio (opzionale)').should('be.visible')

    cy.get('button').contains('Invia').should('be.visible')
    cy.get('button').contains('Annulla').should('be.visible')
  })

  it('should show validation errors for empty required fields', () => {
    cy.get('button').contains('Invia').click()

    cy.get('input[id="emailInput"]:invalid').should('exist')
    cy.get('input[id="amountInput"]:invalid').should('exist')
  })

  it('should show validation error for invalid email format', () => {
    cy.get('input[id="emailInput"]').type('invalid-email')
    cy.get('input[id="amountInput"]').type('10,50')
    cy.get('button').contains('Invia').click()

    cy.get('input[id="emailInput"]:invalid').should('exist')
  })

  it('should validate number format for amount field', () => {
    cy.get('input[id="amountInput"]')
      .should('have.attr', 'type', 'number')
      .should('have.attr', 'step', '0.01')
      .should('have.attr', 'pattern', '^\\d+(\\.\\d{1,2})?$')
  })

  it('should successfully send money with valid data', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendMoneyRequest')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('25.50')
    cy.get('input[placeholder="Aggiungi una nota"]').type('Pagamento per cena')

    cy.get('button').contains('Invia').click()

    cy.wait('@sendMoneyRequest')

    cy.get('#sendModal').should('not.be.visible')

    cy.contains('Denaro inviato con successo!').should('be.visible')
  })

  it('should send money without optional description', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendMoneyRequest')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('15.00')

    cy.get('button').contains('Invia').click()

    cy.wait('@sendMoneyRequest')
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should handle send money error', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendMoneyError')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('1000.00')

    cy.get('button').contains('Invia').click()

    cy.wait('@sendMoneyError')

    cy.get('#sendModal').should('not.be.visible')
  })

  it('should close modal when clicking X button', () => {
    cy.get('button[id="closeSendModal"]').click()
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should close modal when clicking Cancel button', () => {
    cy.get('button').contains('Annulla').click()
    cy.get('#sendModal').should('not.be.visible')
  })

  it('should fail sending money to inexistent email', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendMoneySuccess')

    cy.get('input[id="emailInput"]').type('recipient@example.com')
    cy.get('input[id="amountInput"]').type('50.00')
    cy.get('input[placeholder="Aggiungi una nota"]').type('Test payment')

    cy.get('button').contains('Invia').click()
    cy.wait('@sendMoneySuccess').then((interception) => {
      expect(interception.response?.body).to.deep.equal({ detail: 'Destination wallet not found' })
      expect(interception.response?.statusCode).to.equal(404)
    })

    cy.get('div').contains('Invia denaro').click()

    cy.get('input[id="emailInput"]').should('have.value', '')
    cy.get('input[id="amountInput"]').should('have.value', '')
    cy.get('input[placeholder="Aggiungi una nota"]').should('have.value', '')
  })

  it('should have proper accessibility attributes', () => {
    cy.get('input[id="emailInput"]').should('have.attr', 'required')
    cy.get('input[id="amountInput"]').should('have.attr', 'required')

    cy.get('input[placeholder="Aggiungi una nota"]').should('not.have.attr', 'required')

    cy.get('label').contains('Destinatario').should('exist')
    cy.get('label').contains('Importo').should('exist')
    cy.get('label').contains('Messaggio (opzionale)').should('exist')
  })

  it('should handle decimal amounts correctly', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendDecimalAmount')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('12.75')

    cy.get('button').contains('Invia').click()
    cy.wait('@sendDecimalAmount')
  })

  it('should handle large amounts', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendLargeAmount')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('9999.99')

    cy.get('button').contains('Invia').click()
    cy.wait('@sendLargeAmount')
  })

  it('should emit refresh event after successful send', () => {
    cy.intercept('POST', 'http://0.0.0.0:8000/api/v1/payments/send').as('sendMoneyRefresh')

    cy.get('input[id="emailInput"]').type('mario@example.com')
    cy.get('input[id="amountInput"]').type('25.00')

    cy.get('button').contains('Invia').click()
    cy.wait('@sendMoneyRefresh')
  })
})
