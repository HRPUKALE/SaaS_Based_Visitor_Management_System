import React, { useState, useEffect } from 'react';
import { CheckCircle, Calendar, Clock, User, Mail, Phone, Building, Edit3, Save, X, QrCode, Download } from 'lucide-react';
import { AppointmentBooking } from '../types';
import QRCode from 'qrcode';

interface AppointmentSummaryProps {
  booking: AppointmentBooking;
  onClose: () => void;
  onEdit?: (updatedBooking: AppointmentBooking) => void;
  onSave?: (booking: AppointmentBooking) => Promise<void>;
  isSaving?: boolean;
}

export const AppointmentSummary: React.FC<AppointmentSummaryProps> = ({ 
  booking, 
  onClose, 
  onEdit,
  onSave,
  isSaving = false
}) => {
  const [isEditing, setIsEditing] = useState<string | null>(null);
  const [editedBooking, setEditedBooking] = useState(booking);
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [showQR, setShowQR] = useState(false);
  const [hasBeenSaved, setHasBeenSaved] = useState(false);

  // Generate QR code when component mounts or booking changes
  useEffect(() => {
    const generateQRCode = async () => {
      try {
        const appointmentData = {
          employee: `${editedBooking.employee_name} (${editedBooking.department})`,
          reason: editedBooking.reason,
          date: editedBooking.appointment_date,
          time: editedBooking.appointment_time,
          visitor: editedBooking.visitor_name,
          email: editedBooking.email,
          phone: editedBooking.phone,
          company: 'Kanishka Software'
        };

        const qrData = JSON.stringify(appointmentData, null, 2);
        const qrUrl = await QRCode.toDataURL(qrData, {
          width: 256,
          margin: 2,
          color: {
            dark: '#1f2937',
            light: '#ffffff'
          }
        });
        setQrCodeUrl(qrUrl);
      } catch (error) {
        console.error('Error generating QR code:', error);
      }
    };

    generateQRCode();
  }, [editedBooking]);

  const handleEdit = (field: string) => {
    setIsEditing(field);
  };

  const handleSave = async () => {
    if (onSave) {
      try {
        await onSave(editedBooking);
        setHasBeenSaved(true);
      } catch (error) {
        console.error('Error saving appointment:', error);
      }
    }
  };

  const handleSaveField = (field: string) => {
    setIsEditing(null);
    if (onEdit) {
      onEdit(editedBooking);
    }
  };

  const handleCancel = () => {
    setIsEditing(null);
    setEditedBooking(booking);
  };

  const handleChange = (field: keyof AppointmentBooking, value: string) => {
    setEditedBooking(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const downloadQRCode = () => {
    if (qrCodeUrl) {
      const link = document.createElement('a');
      link.download = `appointment-${editedBooking.visitor_name}-${editedBooking.appointment_date}.png`;
      link.href = qrCodeUrl;
      link.click();
    }
  };

  const handleClose = () => {
    if (isEditing !== null) {
      return; // Don't close if editing
    }
    onClose();
  };

  const renderEditableField = (
    field: keyof AppointmentBooking,
    label: string,
    icon: React.ReactNode,
    value: string
  ) => {
    const isCurrentlyEditing = isEditing === field;

    return (
      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg group hover:bg-gray-100 transition-colors">
        {icon}
        <div className="flex-1">
          <div className="font-medium text-gray-900">{label}</div>
          {isCurrentlyEditing ? (
            <div className="flex items-center gap-2 mt-1">
              <input
                type="text"
                value={editedBooking[field]}
                onChange={(e) => handleChange(field, e.target.value)}
                className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
              />
              <button
                onClick={() => handleSaveField(field)}
                className="p-1 text-green-600 hover:bg-green-100 rounded"
              >
                <Save className="w-4 h-4" />
              </button>
              <button
                onClick={handleCancel}
                className="p-1 text-red-600 hover:bg-red-100 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">{value}</div>
              <button
                onClick={() => handleEdit(field)}
                className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-all"
              >
                <Edit3 className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="text-center p-6 border-b border-gray-200">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Appointment Confirmed!</h2>
          <p className="text-gray-600">Your appointment has been successfully scheduled</p>
          <p className="text-xs text-gray-500 mt-2">Click the edit icon to modify any details</p>
        </div>

        {/* Appointment Details */}
        <div className="p-6">
          <div className="space-y-4 mb-6">
            {renderEditableField(
              'employee_name',
              'Employee',
              <User className="w-5 h-5 text-gray-600" />,
              `${editedBooking.employee_name} (${editedBooking.department})`
            )}

            {renderEditableField(
              'reason',
              'Reason',
              <Building className="w-5 h-5 text-gray-600" />,
              editedBooking.reason
            )}

            {renderEditableField(
              'appointment_date',
              'Date',
              <Calendar className="w-5 h-5 text-gray-600" />,
              editedBooking.appointment_date
            )}

            {renderEditableField(
              'appointment_time',
              'Time',
              <Clock className="w-5 h-5 text-gray-600" />,
              editedBooking.appointment_time
            )}

            {renderEditableField(
              'visitor_name',
              'Visitor Name',
              <User className="w-5 h-5 text-gray-600" />,
              editedBooking.visitor_name
            )}

            {renderEditableField(
              'email',
              'Email',
              <Mail className="w-5 h-5 text-gray-600" />,
              editedBooking.email
            )}

            {renderEditableField(
              'phone',
              'Phone',
              <Phone className="w-5 h-5 text-gray-600" />,
              editedBooking.phone
            )}
          </div>

          {/* QR Code Section */}
          <div className="border-t border-gray-200 pt-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <QrCode className="w-5 h-5" />
                QR Code
              </h3>
              <button
                onClick={() => setShowQR(!showQR)}
                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                {showQR ? 'Hide' : 'Show'} QR
              </button>
            </div>

            {showQR && qrCodeUrl && (
              <div className="text-center">
                <div className="inline-block p-4 bg-white border-2 border-gray-200 rounded-lg">
                  <img 
                    src={qrCodeUrl} 
                    alt="Appointment QR Code" 
                    className="w-48 h-48 mx-auto"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-2 mb-3">
                  Scan this QR code to share appointment details
                </p>
                <button
                  onClick={downloadQRCode}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download QR Code
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200">
          <div className="flex gap-3">
            <button
              onClick={handleSave}
              disabled={isSaving || isEditing !== null}
              className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Saving...' : hasBeenSaved ? 'Saved!' : 'Save Appointment'}
            </button>
            <button
              onClick={handleClose}
              disabled={isEditing !== null}
              className="flex-1 px-4 py-3 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isEditing ? 'Finish editing to close' : 'Close'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};