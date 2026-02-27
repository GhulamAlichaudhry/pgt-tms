# 🎨 MODERN INVOICE - SETUP GUIDE

## ✅ INVOICE UPDATED!

Your invoice is now **modern, elegant, and one-page** with:

✅ Professional blue color scheme  
✅ Compact layout (fits on one page)  
✅ All contact details (phone, mobile, email, address)  
✅ Logo support (ready to add)  
✅ Modern typography  
✅ Clean, organized sections  
✅ Professional formatting  

---

## 📋 WHAT'S INCLUDED NOW

### Header Section:
- ✅ Company logo (if added)
- ✅ Company name in large, bold blue text
- ✅ Tagline
- ✅ **Full address**
- ✅ **Phone number**
- ✅ **Mobile number**
- ✅ **Email address**
- ✅ **Website**
- ✅ **NTN (Tax ID)**

### Invoice Details:
- ✅ Invoice number (prominent)
- ✅ Invoice date
- ✅ Due date

### Client & Trip Info (Side by Side):
- ✅ Client name, contact, address, phone, email
- ✅ Trip reference, date, vehicle, driver
- ✅ From → To locations
- ✅ Cargo type and weight

### Charges:
- ✅ Service description
- ✅ Quantity/tonnage
- ✅ Rate
- ✅ Amount
- ✅ Subtotal, tax, discount
- ✅ **Total in large blue text**

### Payment Info:
- ✅ Payment terms
- ✅ Due date
- ✅ **Complete bank details:**
  - Bank name
  - Branch
  - Account title
  - Account number
  - IBAN

### Footer:
- ✅ Thank you message
- ✅ Contact info for queries
- ✅ Generation timestamp

---

## 🎨 COLOR SCHEME

**Modern Blue Theme:**
- Primary: `#1e40af` (Professional Blue)
- Light: `#eff6ff` (Light Blue Background)
- Text: `#475569` (Dark Gray)
- Subtle: `#64748b` (Medium Gray)
- Borders: `#cbd5e1` (Light Gray)

---

## 🖼️ HOW TO ADD YOUR LOGO

### Step 1: Prepare Your Logo

**Requirements:**
- Format: PNG (with transparent background recommended)
- Size: 300x300 pixels or larger
- Aspect ratio: Square or rectangular
- File size: Under 1MB

### Step 2: Add Logo File

**Option A: Using File Explorer**
1. Open folder: `backend/static/`
2. Copy your logo file
3. Rename it to: `logo.png`
4. Done!

**Option B: Using Command**
```bash
# Copy your logo to the static folder
copy "C:\path\to\your\logo.png" "backend\static\logo.png"
```

### Step 3: Restart Backend

The logo will automatically appear on all invoices!

**If logo doesn't show:**
- Check file name is exactly `logo.png`
- Check file is in `backend/static/` folder
- Restart backend server
- Generate new invoice

---

## ⚙️ CUSTOMIZE COMPANY DETAILS

### Update Company Information

**File:** `backend/enhanced_invoice_generator.py`

**Find this section (around line 20):**

```python
self.company_info = {
    "name": "PGT INTERNATIONAL (PVT) LTD",
    "tagline": "Excellence in Transportation & Logistics",
    "address": "Office # 7, 1st Floor, Haji Yousuf Plaza, Near Memon Masjid, M.A Jinnah Road, Karachi",
    "phone": "+92-21-32412345",
    "mobile": "+92-300-1234567",
    "email": "info@pgtinternational.com",
    "website": "www.pgtinternational.com",
    "ntn": "NTN: 1234567-8",
    "bank_details": {
        "bank_name": "Meezan Bank Limited",
        "branch": "M.A. Jinnah Road Branch",
        "account_title": "PGT International (Pvt) Ltd",
        "account_number": "01234567890123",
        "iban": "PK12 MEZN 0001 2345 6789 0123"
    }
}
```

### What to Update:

1. **Company Name** - Your official company name
2. **Tagline** - Your company slogan
3. **Address** - Your complete office address
4. **Phone** - Your landline number
5. **Mobile** - Your mobile number
6. **Email** - Your company email
7. **Website** - Your website URL
8. **NTN** - Your tax registration number
9. **Bank Name** - Your bank name
10. **Branch** - Your bank branch
11. **Account Title** - Account holder name
12. **Account Number** - Your account number
13. **IBAN** - Your IBAN number

### After Updating:
1. Save the file
2. Restart backend server
3. Generate new invoice
4. All details will appear!

---

## 🎯 INVOICE FEATURES

### Modern Design Elements:

1. **One-Page Layout**
   - Compact spacing
   - Efficient use of space
   - Everything fits on one page

2. **Professional Colors**
   - Blue theme for trust and professionalism
   - Light backgrounds for readability
   - High contrast for clarity

3. **Clear Hierarchy**
   - Important info stands out
   - Logical flow from top to bottom
   - Easy to scan and read

4. **Complete Information**
   - All contact details visible
   - Full bank information
   - Clear payment terms

5. **Modern Typography**
   - Clean fonts
   - Appropriate sizes
   - Good spacing

---

## 📱 CONTACT DETAILS DISPLAY

### Header Shows:
```
PGT INTERNATIONAL (PVT) LTD
Excellence in Transportation & Logistics

Address: Office # 7, 1st Floor, Haji Yousuf Plaza, Near Memon Masjid, M.A Jinnah Road, Karachi
Phone: +92-21-32412345 | Mobile: +92-300-1234567 | Email: info@pgtinternational.com | Web: www.pgtinternational.com
NTN: 1234567-8
```

### Footer Shows:
```
Thank you for your business! | For queries: +92-21-32412345 or info@pgtinternational.com | Generated: 27-Feb-2026 10:30 PM
```

---

## 🏦 BANK DETAILS DISPLAY

### Payment Info Section Shows:
```
BANK DETAILS
Bank: Meezan Bank Limited
Branch: M.A. Jinnah Road Branch
Account: PGT International (Pvt) Ltd
A/C #: 01234567890123
IBAN: PK12 MEZN 0001 2345 6789 0123
```

---

## 🎨 CUSTOMIZATION OPTIONS

### Change Colors:

**File:** `backend/enhanced_invoice_generator.py`

**Find and replace these color codes:**
- `#1e40af` - Primary blue (company name, totals)
- `#eff6ff` - Light blue backgrounds
- `#475569` - Dark text
- `#64748b` - Medium gray text
- `#cbd5e1` - Borders

**Popular Color Schemes:**

**Red Theme:**
- Primary: `#dc2626`
- Light: `#fee2e2`

**Green Theme:**
- Primary: `#059669`
- Light: `#d1fae5`

**Purple Theme:**
- Primary: `#7c3aed`
- Light: `#ede9fe`

### Change Fonts:

Replace `Helvetica` with:
- `Helvetica-Bold` for bold
- `Times-Roman` for serif
- `Courier` for monospace

---

## 📏 LAYOUT SPECIFICATIONS

### Page Size:
- Letter (8.5" × 11")
- Margins: 0.4" (left/right), 0.3" (top/bottom)

### Sections:
1. Header: ~1.5"
2. Invoice Info: ~0.5"
3. Client/Trip: ~1"
4. Charges: ~2"
5. Totals: ~0.5"
6. Payment Info: ~1"
7. Footer: ~0.3"

**Total: Fits perfectly on one page!**

---

## ✅ TESTING CHECKLIST

After customization:

- [ ] Company name correct
- [ ] All contact details correct
- [ ] Logo appears (if added)
- [ ] Bank details correct
- [ ] Colors look professional
- [ ] Everything fits on one page
- [ ] Text is readable
- [ ] No overlapping elements
- [ ] Footer shows correct info

---

## 🚀 QUICK START

### 1. Add Your Logo (Optional)
```bash
# Copy logo to static folder
copy "your-logo.png" "backend\static\logo.png"
```

### 2. Update Company Details
- Open `backend/enhanced_invoice_generator.py`
- Update company_info section
- Save file

### 3. Restart Backend
```bash
# Backend will restart automatically
# Or manually restart if needed
```

### 4. Test Invoice
- Go to Receivables page
- Click download button
- Check invoice looks perfect!

---

## 💡 TIPS

### For Best Results:

1. **Logo:**
   - Use high-quality PNG
   - Transparent background works best
   - Square or horizontal orientation

2. **Contact Details:**
   - Use complete address
   - Include area code in phone
   - Use professional email

3. **Bank Details:**
   - Double-check account number
   - Verify IBAN format
   - Include branch name

4. **Colors:**
   - Stick to 2-3 colors max
   - Use professional colors
   - Ensure good contrast

5. **Testing:**
   - Generate test invoice
   - Print to check layout
   - Verify all details

---

## 🎉 RESULT

Your invoices now look:

✅ **Professional** - Modern design and colors  
✅ **Complete** - All contact and bank details  
✅ **Elegant** - Clean layout and typography  
✅ **One-Page** - Everything fits perfectly  
✅ **Branded** - Your logo and colors  
✅ **Clear** - Easy to read and understand  

---

## 📞 NEED HELP?

### Common Issues:

**Logo not showing?**
- Check file name: `logo.png`
- Check location: `backend/static/`
- Restart backend

**Details not updating?**
- Save the file after editing
- Restart backend
- Clear browser cache

**Layout issues?**
- Check text length
- Reduce font sizes if needed
- Adjust spacing

---

**Your invoices are now modern, elegant, and professional!** 🎨✨

**Status:** READY TO USE  
**Design:** Modern & Elegant  
**Layout:** One Page  
**Contact Details:** Complete  
**Logo:** Ready to Add
