# Vehicle Types Update

## Overview
Updated the vehicle types in Fleet Management to reflect the common vehicle types used by PGT International.

## Changes Made

### Vehicle Types List
Simplified and standardized the vehicle types to the three main categories used in operations:

1. **40 Ft Container** - Standard 40-foot shipping container
2. **20 Ft Container** - Standard 20-foot shipping container  
3. **Flat Bed** - Flat bed trailer for various cargo types
4. **Custom** - Option to enter any other vehicle type manually

### Previous Vehicle Types (Removed)
- Container Truck
- Trailer
- Pickup
- Van

These were removed as they are not commonly used in your operations. If needed, they can be added using the "Custom" option.

## Why This Change?

### Based on Your Fleet Data
Looking at your vehicle list, the majority of vehicles fall into these categories:
- Multiple 40 Ft Containers
- Multiple Flat Beds
- Some 20 Ft Containers

### Benefits
1. **Simplified Selection**: Only shows the vehicle types you actually use
2. **Faster Data Entry**: Less scrolling through unused options
3. **Consistency**: Standardized naming across the system
4. **Flexibility**: Custom option still available for special cases

## How to Use

### Adding a Standard Vehicle
1. Go to Settings page
2. Click "Add Vehicle" button
3. Select vehicle type from dropdown:
   - 40 Ft Container
   - 20 Ft Container
   - Flat Bed
4. Enter vehicle number and capacity
5. Click "Add Vehicle"

### Adding a Custom Vehicle Type
1. Go to Settings page
2. Click "Add Vehicle" button
3. Select "Custom (Enter Manually)" from dropdown
4. A text field will appear
5. Enter your custom vehicle type (e.g., "Refrigerated Container", "Low Bed Trailer")
6. Enter vehicle number and capacity
7. Click "Add Vehicle"

## Vehicle Type Standards

### 40 Ft Container
- Standard length: 40 feet
- Typical capacity: 25-30 tons
- Most common for long-haul transport
- Used for containerized cargo

### 20 Ft Container
- Standard length: 20 feet
- Typical capacity: 20-25 tons
- Used for smaller loads
- More maneuverable in tight spaces

### Flat Bed
- Open platform trailer
- Variable capacity: 15-40 tons
- Used for oversized cargo
- Flexible loading/unloading

## Examples from Your Fleet

Based on the image you provided, your fleet includes:
- **5x 40 Ft Container** vehicles
- **8x Flat Bed** vehicles
- **1x 20 Ft Container** vehicle
- **8x 40 ft Containers** (additional units)

Total: 22 vehicles across 3 main types

## Future Additions

If you need to add more vehicle types permanently, you can:

1. **Option 1**: Use Custom type for now
2. **Option 2**: Request to add it to the standard list
3. **Option 3**: Edit `frontend/src/pages/Settings.js` and add new options

### To Add a New Standard Type:
```javascript
<option value="Your Vehicle Type">Your Vehicle Type</option>
```

Add this line in the vehicle type dropdown section.

## File Modified
- `frontend/src/pages/Settings.js` - Updated vehicle type dropdown options

## Testing

### Test Adding Each Vehicle Type:
1. ✅ 40 Ft Container
2. ✅ 20 Ft Container
3. ✅ Flat Bed
4. ✅ Custom type

### Verify:
- Dropdown shows only 4 options (3 standard + Custom)
- Custom field appears when "Custom" is selected
- Custom field hides when standard type is selected
- Vehicle is created successfully with selected type
- Vehicle type displays correctly in vehicle list

## Status
✅ **COMPLETE** - Vehicle types updated to match PGT International's common fleet types

## Notes
- Existing vehicles in the database are not affected
- Only new vehicle additions will use the updated dropdown
- Custom option provides flexibility for special cases
- Vehicle types are stored as text, so any value is technically valid
