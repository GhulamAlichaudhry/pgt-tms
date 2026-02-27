# Requirements Document

## Introduction

Transform the existing PGT Transport Management System into a comprehensive master accounting-driven management system. The system must provide complete financial visibility with proper separation between income (client/rent) and expenses (vendor/operational), implementing a robust ledger engine for all financial transactions, and delivering real-time financial insights through an owner-focused dashboard.

## Glossary

- **System**: The PGT TMS Accounting Management System
- **Ledger_Engine**: Core accounting engine that maintains running balances using Opening Balance + Credits - Debits = Running Balance formula
- **Client_Ledger**: Receivables ledger tracking money owed to the company
- **Vendor_Ledger**: Payables ledger tracking money the company owes
- **Cash_Bank_Ledger**: Ledger tracking actual cash and bank account balances
- **Owner_Dashboard**: Master dashboard providing 10-second financial overview
- **Rent_Income**: Revenue from client agreements and transport services
- **Vendor_Charges**: All costs associated with vendors and suppliers
- **Net_Job_Result**: Revenue minus all job-related costs (fuel, advance, other costs)
- **Daily_Cash_Flow**: Daily income minus daily outgoing payments
- **Total_Receivable**: Sum of all positive client ledger balances
- **Total_Payable**: Sum of all positive vendor ledger balances

## Requirements

### Requirement 1: Client/Rent Module Implementation

**User Story:** As a business owner, I want to track all client receivables and rent agreements, so that I can monitor income and outstanding payments.

#### Acceptance Criteria

1. WHEN a client agreement is created, THE System SHALL generate a unique Client ID and store agreement details
2. WHEN rent is raised for a client, THE System SHALL create a debit entry in the Client_Ledger
3. WHEN payment is received from a client, THE System SHALL create a credit entry in the Client_Ledger
4. THE System SHALL calculate client balance using the formula: Previous Balance + Rent Raised - Payment Received
5. THE System SHALL ensure vendor charges never reduce rent income amounts
6. WHEN displaying client information, THE System SHALL show Client ID, Agreement Reference, Date, Rent Amount, Payment Received, and Current Balance

### Requirement 2: Vendor Module Implementation

**User Story:** As a business owner, I want to track all vendor payables and expenses, so that I can monitor what the company owes and manage cash flow.

#### Acceptance Criteria

1. WHEN a vendor is registered, THE System SHALL generate a unique Vendor ID and store vendor details
2. WHEN a vendor charge is recorded, THE System SHALL create a credit entry in the Vendor_Ledger
3. WHEN payment is made to a vendor, THE System SHALL create a debit entry in the Vendor_Ledger
4. THE System SHALL calculate vendor balance using the formula: Previous Balance + Charges - Payments
5. THE System SHALL ensure all vendor-related costs remain in the vendor module and do not mix with rent calculations
6. WHEN displaying vendor information, THE System SHALL show Vendor ID, Expense Type, Date, Charge Amount, Payment Made, and Current Balance

### Requirement 3: Operations/Job Module Integration

**User Story:** As an operations manager, I want to track job profitability, so that I can understand which operations are profitable.

#### Acceptance Criteria

1. WHEN a job is completed, THE System SHALL calculate Net Job Result using the formula: Revenue - (Fuel + Advance + Other Costs)
2. THE System SHALL feed job results into income, expense, and profit reports
3. WHEN job costs are recorded, THE System SHALL categorize them appropriately between operational expenses and vendor charges
4. THE System SHALL maintain job-level profitability tracking for analysis

### Requirement 4: Enhanced Expense Module

**User Story:** As a financial manager, I want to track all non-vendor operational expenses, so that I can monitor total company expenses.

#### Acceptance Criteria

1. WHEN an operational expense is recorded, THE System SHALL categorize it as non-vendor expense
2. THE System SHALL calculate Total Expenses as the sum of all expense entries
3. WHEN displaying expenses, THE System SHALL separate vendor expenses from operational expenses
4. THE System SHALL provide expense categorization and filtering capabilities

### Requirement 5: Mandatory Ledger Engine Implementation

**User Story:** As a business owner, I want all financial transactions to use a consistent ledger system, so that I can trust the accuracy of financial data.

#### Acceptance Criteria

1. THE System SHALL implement the Ledger_Engine for all financial entities
2. THE System SHALL calculate running balances using the formula: Opening Balance + Credits - Debits = Running Balance
3. THE System SHALL maintain separate ledgers for Client_Ledger, Vendor_Ledger, and Cash_Bank_Ledger
4. WHEN any financial transaction occurs, THE System SHALL update the appropriate ledger immediately
5. THE System SHALL ensure ledger entries are immutable once created
6. THE System SHALL provide audit trail for all ledger modifications

### Requirement 6: Master Financial Calculations

**User Story:** As a business owner, I want real-time financial calculations, so that I can make informed business decisions.

#### Acceptance Criteria

1. THE System SHALL calculate Total Receivable as the sum of all Client_Ledger balances where balance > 0
2. THE System SHALL calculate Total Payable as the sum of all Vendor_Ledger balances where balance > 0
3. THE System SHALL calculate Total Income as Rent_Income + Operational Revenue
4. THE System SHALL calculate Total Expenses as Vendor_Charges + Office Expenses + Operational Costs
5. THE System SHALL calculate Net Profit as Total Income - Total Expenses
6. WHEN any financial transaction occurs, THE System SHALL update all master calculations in real-time

### Requirement 7: Daily Cash Flow Tracking

**User Story:** As a business owner, I want to track daily cash movements, so that I can monitor daily financial performance.

#### Acceptance Criteria

1. THE System SHALL calculate Daily Income as the sum of all payments received today
2. THE System SHALL calculate Daily Outgoing as the sum of all payments made today
3. THE System SHALL calculate Daily Net as Daily Income - Daily Outgoing
4. WHEN displaying daily cash flow, THE System SHALL show date-filtered income and expense breakdowns
5. THE System SHALL provide historical daily cash flow analysis

### Requirement 8: Owner Dashboard Implementation

**User Story:** As a business owner, I want a comprehensive dashboard that shows key financial metrics in 10 seconds, so that I can quickly assess business health.

#### Acceptance Criteria

1. WHEN the Owner_Dashboard loads, THE System SHALL display Total Receivable, Total Payable, Net Profit/Loss, and Cash/Bank Balance as top summary cards
2. THE System SHALL display today's snapshot showing Today's Income, Today's Expenses, and Today's Net Cash Flow
3. THE System SHALL show breakdowns including Top 5 Clients by Receivable and Top 5 Vendors by Payable
4. THE System SHALL display expense charts and income vs expense trends
5. THE System SHALL show alerts for overdue receivables, outstanding vendor balances, and negative cash flow days
6. WHEN dashboard data changes, THE System SHALL update all metrics in real-time

### Requirement 9: Comprehensive Reporting System

**User Story:** As a business manager, I want detailed financial reports, so that I can analyze business performance and meet compliance requirements.

#### Acceptance Criteria

1. THE System SHALL generate Client Ledger reports with date filtering capabilities
2. THE System SHALL generate Vendor Ledger reports with date filtering capabilities
3. THE System SHALL generate Profit & Loss statements for specified periods
4. THE System SHALL generate Daily Cash Flow reports with date range selection
5. THE System SHALL generate Monthly Summary reports
6. THE System SHALL export all reports in PDF and Excel formats
7. WHEN generating reports, THE System SHALL ensure data accuracy and consistency with ledger balances

### Requirement 10: Data Validation and Business Rules

**User Story:** As a system administrator, I want robust data validation, so that financial data remains accurate and consistent.

#### Acceptance Criteria

1. THE System SHALL prevent manual editing of calculated fields
2. THE System SHALL populate all dropdowns dynamically from current data
3. THE System SHALL provide date-based filtering on all financial screens
4. THE System SHALL restrict duplicate critical entries based on business rules
5. THE System SHALL implement role-based access control for Owner, Manager, and Operator roles
6. WHEN invalid data is entered, THE System SHALL display clear error messages and prevent submission

### Requirement 11: Technical Architecture Requirements

**User Story:** As a system architect, I want entity-agnostic design with real-time capabilities, so that the system is scalable and maintainable.

#### Acceptance Criteria

1. THE System SHALL implement entity-agnostic design with no hardcoded business names
2. THE System SHALL provide real-time calculation updates across all modules
3. THE System SHALL ensure all transactions are audit-safe with proper logging
4. THE System SHALL implement scalable architecture supporting future growth
5. THE System SHALL maintain consistent red color scheme (#dc2626) across the modern UI
6. WHEN system load increases, THE System SHALL maintain performance standards

### Requirement 12: Data Migration and Integration

**User Story:** As a system administrator, I want seamless migration from the existing system, so that historical data is preserved and accessible.

#### Acceptance Criteria

1. WHEN migrating existing trip data, THE System SHALL convert it to the new accounting structure
2. THE System SHALL preserve all historical financial transactions during migration
3. THE System SHALL map existing vendor and client data to new ledger format
4. THE System SHALL validate data integrity after migration
5. THE System SHALL provide rollback capabilities during migration process