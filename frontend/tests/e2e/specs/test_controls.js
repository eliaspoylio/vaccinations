describe('Test controls', () => {
    it('Visits the app root url', () => {
        cy.visit('/')
        cy.contains('button', 'Update dashboard')
        cy.should('not.contain', '12662')
    })
    it('Clicks the button', () => {
        cy.visit('/')
        cy.get('.button').click()
        cy.wait(2000)
        cy.contains('12662')
    }) 
})