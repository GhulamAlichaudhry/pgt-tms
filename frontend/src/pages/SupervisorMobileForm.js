import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Camera,
  Upload,
  CheckCircle,
  Truck,
  MapPin,
  Package,
  Calendar,
  FileText,
  AlertCircle
} from 'lucide-react';

const SupervisorMobileForm = () => {
  const [vehicles, setVehicles] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [biltyImage, setBiltyImage] = useState(null);
  const [biltyPreview, setBiltyPreview] = useState(null);

  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    vehicle_id: '',
    client_id: '',
    category_product: '',
    source_location: '',
    destination_location: '',
    driver_operator: '',
    reference_no: '',
    total_tonnage: ''
  });

  const commonProducts = [
    'Lactose',
    'Pumice Stone',
    'Cotton Bales',
    'Soyabeen Meal',
    'Feed',
    'Feed Pallets',
    'Other'
  ];

  const commonDestinations = [
    'Karachi',
    'Lahore',
    'Islamabad',
    'Faisalabad',
    'Multan',
    'Rawalpindi',
    'Gujranwala',
    'Peshawar',
    'Quetta',
    'Sialkot',
    'Bhalwal',
    'Other'
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const [vehiclesRes, clientsRes] = await Promise.all([
        axios.get('/vehicles/', { headers: { 'Authorization': `Bearer ${token}` } }),
        axios.get('/clients/', { headers: { 'Authorization': `Bearer ${token}` } })
      ]);
      setVehicles(vehiclesRes.data);
      setClients(clientsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load form data');
    } finally {
      setLoading(false);
    }
  };

  const handleImageCapture = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Image size must be less than 5MB');
        return;
      }

      // Validate file type
      if (!file.type.startsWith('image/')) {
        toast.error('Please select an image file');
        return;
      }

      setBiltyImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setBiltyPreview(reader.result);
      };
      reader.readAsDataURL(file);
      
      toast.success('Bilty image captured!');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.vehicle_id) {
      toast.error('Please select a vehicle');
      return;
    }
    if (!formData.client_id) {
      toast.error('Please select a client');
      return;
    }
    if (!formData.category_product) {
      toast.error('Please select a product');
      return;
    }
    if (!formData.destination_location) {
      toast.error('Please select destination');
      return;
    }
    if (!formData.reference_no) {
      toast.error('Please enter Bilty number');
      return;
    }
    if (!biltyImage) {
      toast.error('Please upload Bilty image');
      return;
    }

    setSubmitting(true);
    
    try {
      const token = localStorage.getItem('token');
      
      // Note: In production, this would upload the image to a server
      // For now, we'll just submit the trip data
      // The freight amounts are NOT sent from supervisor's device
      
      const tripData = {
        date: new Date(formData.date).toISOString(),
        reference_no: formData.reference_no,
        vehicle_id: parseInt(formData.vehicle_id),
        client_id: parseInt(formData.client_id),
        vendor_id: 1, // Default vendor, will be updated by admin
        category_product: formData.category_product,
        source_location: formData.source_location || 'Port',
        destination_location: formData.destination_location,
        driver_operator: formData.driver_operator || 'TBD',
        total_tonnage: parseFloat(formData.total_tonnage) || 0,
        
        // SECURITY: Freight amounts set to 0 - Admin will update later
        // Supervisor NEVER sees or enters freight amounts
        client_freight: 0,
        vendor_freight: 0,
        freight_mode: 'total',
        
        notes: `Submitted by Supervisor - Bilty: ${formData.reference_no}`
      };

      await axios.post('/trips/', tripData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      toast.success('Trip submitted successfully! Admin will add freight details.');
      
      // Reset form
      setFormData({
        date: new Date().toISOString().split('T')[0],
        vehicle_id: '',
        client_id: '',
        category_product: '',
        source_location: '',
        destination_location: '',
        driver_operator: '',
        reference_no: '',
        total_tonnage: ''
      });
      setBiltyImage(null);
      setBiltyPreview(null);
      
    } catch (error) {
      console.error('Error submitting trip:', error);
      toast.error('Failed to submit trip');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-4">
      {/* High Contrast Header for Outdoor Visibility */}
      <div className="bg-red-600 rounded-2xl p-6 mb-6 shadow-2xl">
        <div className="flex items-center justify-center space-x-3">
          <Truck className="h-10 w-10 text-white" />
          <div className="text-center">
            <h1 className="text-3xl font-bold text-white">PGT TRIP ENTRY</h1>
            <p className="text-red-100 text-sm">Port Supervisor Form</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Date */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Calendar className="h-6 w-6 mr-3 text-red-600" />
            Date
          </label>
          <input
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({...formData, date: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200"
            required
          />
        </div>

        {/* Vehicle Selection */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Truck className="h-6 w-6 mr-3 text-red-600" />
            Vehicle Number
          </label>
          <select
            value={formData.vehicle_id}
            onChange={(e) => setFormData({...formData, vehicle_id: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200 bg-white"
            required
          >
            <option value="">Select Vehicle</option>
            {vehicles.map(vehicle => (
              <option key={vehicle.id} value={vehicle.id}>
                {vehicle.vehicle_no} - {vehicle.vehicle_type}
              </option>
            ))}
          </select>
        </div>

        {/* Client Selection */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Package className="h-6 w-6 mr-3 text-red-600" />
            Client Name
          </label>
          <select
            value={formData.client_id}
            onChange={(e) => setFormData({...formData, client_id: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200 bg-white"
            required
          >
            <option value="">Select Client</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
        </div>

        {/* Product Selection */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Package className="h-6 w-6 mr-3 text-red-600" />
            Product
          </label>
          <select
            value={formData.category_product}
            onChange={(e) => setFormData({...formData, category_product: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200 bg-white"
            required
          >
            <option value="">Select Product</option>
            {commonProducts.map(product => (
              <option key={product} value={product}>
                {product}
              </option>
            ))}
          </select>
        </div>

        {/* Destination Selection */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <MapPin className="h-6 w-6 mr-3 text-red-600" />
            Destination
          </label>
          <select
            value={formData.destination_location}
            onChange={(e) => setFormData({...formData, destination_location: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200 bg-white"
            required
          >
            <option value="">Select Destination</option>
            {commonDestinations.map(dest => (
              <option key={dest} value={dest}>
                {dest}
              </option>
            ))}
          </select>
        </div>

        {/* Tonnage */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Package className="h-6 w-6 mr-3 text-red-600" />
            Total Tonnage
          </label>
          <input
            type="number"
            step="0.01"
            value={formData.total_tonnage}
            onChange={(e) => setFormData({...formData, total_tonnage: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200"
            placeholder="Enter tonnage"
          />
        </div>

        {/* Bilty Number */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <FileText className="h-6 w-6 mr-3 text-red-600" />
            Bilty Number
          </label>
          <input
            type="text"
            value={formData.reference_no}
            onChange={(e) => setFormData({...formData, reference_no: e.target.value})}
            className="w-full text-2xl p-4 border-4 border-gray-300 rounded-xl focus:border-red-600 focus:ring-4 focus:ring-red-200"
            placeholder="Enter Bilty #"
            required
          />
        </div>

        {/* Bilty Image Upload - Large Button for Outdoor Use */}
        <div className="bg-white rounded-2xl p-6 shadow-xl">
          <label className="flex items-center text-xl font-bold text-gray-900 mb-3">
            <Camera className="h-6 w-6 mr-3 text-red-600" />
            Bilty Photo
          </label>
          
          {!biltyPreview ? (
            <label className="flex flex-col items-center justify-center w-full h-64 border-4 border-dashed border-red-600 rounded-2xl cursor-pointer bg-red-50 hover:bg-red-100 transition-all">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Camera className="h-20 w-20 text-red-600 mb-4" />
                <p className="text-2xl font-bold text-red-600 mb-2">TAP TO CAPTURE</p>
                <p className="text-lg text-gray-600">Take photo of Bilty</p>
              </div>
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleImageCapture}
                className="hidden"
              />
            </label>
          ) : (
            <div className="relative">
              <img
                src={biltyPreview}
                alt="Bilty Preview"
                className="w-full h-64 object-cover rounded-2xl border-4 border-green-600"
              />
              <div className="absolute top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-full flex items-center space-x-2">
                <CheckCircle className="h-5 w-5" />
                <span className="font-bold">Captured</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setBiltyImage(null);
                  setBiltyPreview(null);
                }}
                className="absolute bottom-4 right-4 bg-red-600 text-white px-6 py-3 rounded-full font-bold text-lg hover:bg-red-700"
              >
                Retake
              </button>
            </div>
          )}
        </div>

        {/* Security Notice */}
        <div className="bg-yellow-50 border-4 border-yellow-400 rounded-2xl p-4">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-6 w-6 text-yellow-600 flex-shrink-0 mt-1" />
            <div>
              <p className="text-sm font-medium text-yellow-800">
                Note: Freight amounts will be added by Admin. You only need to enter trip details and upload Bilty photo.
              </p>
            </div>
          </div>
        </div>

        {/* Submit Button - Extra Large for Outdoor Use */}
        <button
          type="submit"
          disabled={submitting || !biltyImage}
          className={`w-full text-3xl font-bold py-8 rounded-2xl shadow-2xl transition-all ${
            submitting || !biltyImage
              ? 'bg-gray-400 text-gray-700 cursor-not-allowed'
              : 'bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-700 hover:to-red-800 active:scale-95'
          }`}
        >
          {submitting ? (
            <div className="flex items-center justify-center space-x-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-4 border-white"></div>
              <span>SUBMITTING...</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-3">
              <Upload className="h-10 w-10" />
              <span>SUBMIT TRIP</span>
            </div>
          )}
        </button>
      </form>

      {/* Success Message Space */}
      <div className="h-20"></div>
    </div>
  );
};

export default SupervisorMobileForm;
