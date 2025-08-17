// @ts-check
const { test, expect } = require('@playwright/test');

test.beforeEach(async ({ page }) => {
  // Navigate to the app and wait for the data to load
  await page.goto('/');
  await page.waitForResponse('**/api/adp');
});

test('homepage has correct title and loads data table', async ({ page }) => {
  // Check that the main heading is visible and has the correct text
  await expect(page.locator('h1')).toHaveText('Keeper League Custom ADP');

  // Check that the ADP table is rendered
  const table = page.getByTestId('adp-table');
  await expect(table).toBeVisible();

  // Check that the table has at least one row of data
  const tableBodyRows = table.locator('tbody tr');
  expect(await tableBodyRows.count()).toBeGreaterThan(0);
});

test('search functionality filters the table', async ({ page }) => {
  const searchBar = page.locator('.search-bar');
  const tableBody = page.getByTestId('adp-table').locator('tbody');

  // Use pressSequentially to simulate user typing
  await searchBar.pressSequentially("Ja'Marr Chase", { delay: 100 });

  // Wait for the table to contain the expected player, which is the most robust check
  await expect(tableBody).toContainText("Ja'Marr Chase");

  // Assert that only one row is visible
  await expect(tableBody.locator('tr')).toHaveCount(1);

  // Clear the search and verify the table resets
  await searchBar.clear();
  
  // Wait for the table to reset by asserting the row count is no longer 1
  await expect(tableBody.locator('tr')).not.toHaveCount(1);
  
});

test('sort functionality works correctly', async ({ page }) => {
  const adpHeader = page.locator('th', { hasText: 'ADP' });
  const tableBody = page.getByTestId('adp-table').locator('tbody');

  // Helper to get ADP values from the table
  const getAdpValues = () => tableBody.locator('tr').evaluateAll(rows => 
    rows.map(row => {
      const text = (/** @type {HTMLTableRowElement} */ (row).cells[1].textContent || '').trim();
      if (text === 'N/A') return Infinity;
      return parseFloat(text);
    })
  );

  const initialAdp = await getAdpValues();

  // Click to sort descending
  await adpHeader.click();
  const descendingAdp = await getAdpValues();
  const sortedDescending = [...initialAdp].sort((a, b) => b - a);
  expect(descendingAdp).toEqual(sortedDescending);

  // Click again to sort ascending
  await adpHeader.click();
  const ascendingAdp = await getAdpValues();
  const sortedAscending = [...initialAdp].sort((a, b) => a - b);
  expect(ascendingAdp).toEqual(sortedAscending);
});
