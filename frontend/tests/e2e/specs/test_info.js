describe('Test header', () => {
  it('Visits the app root url', () => {
    cy.visit('/')
    cy.contains('h2', 'Vaccination dashboard')
  })
})
