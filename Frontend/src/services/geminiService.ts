import { ChatMessage, AppointmentState, AppointmentBooking } from '../types';
import { apiService } from './api';

export class GeminiService {
  private static readonly API_KEY = 'AIzaSyAIhfGYSuOz0lvEtZvNUkUeOzBVi3cDsH0';
  private static readonly API_URL = '/gemini-api/v1beta/models/gemini-2.0-flash:generateContent';

  static async processConversation(
    messages: ChatMessage[],
    state: AppointmentState
  ): Promise<{
    response: string;
    updatedState: AppointmentState;
    needsConfirmation: boolean;
    finalBooking?: AppointmentBooking;
  }> {
    try {
      console.log('🤖 Gemini processing conversation...');
      
      // Build conversation for Gemini with enhanced system prompt
      const geminiMessages = await this.buildGeminiConversation(messages, state);
      
      // Call Gemini API
      const geminiResponse = await this.callGeminiAPI(geminiMessages);
      console.log('🤖 Gemini raw response:', geminiResponse);
      
      // Check if Gemini is providing a final booking JSON
      const finalBooking = this.extractFinalBookingJSON(geminiResponse);
      if (finalBooking) {
        console.log('🎉 Final booking JSON extracted:', finalBooking);
        // Validate time: if today and time is in the past, reject
        const now = new Date();
        const [selectedHour, selectedMinute] = finalBooking.appointment_time.split(":").map(Number);
        const selectedDate = new Date();
        selectedDate.setHours(selectedHour, selectedMinute, 0, 0);
        const todayStr = now.toISOString().split('T')[0];
        if (finalBooking.appointment_date === todayStr && selectedDate < now) {
          return {
            response: 'You cannot book an appointment for a time that has already passed today. Please select a future time.',
            updatedState: state,
            needsConfirmation: false
          };
        }
        // Update state with final booking data
        const updatedState: AppointmentState = {
          employee_name: finalBooking.employee_name,
          department: finalBooking.department,
          reason: finalBooking.reason,
          appointment_time: finalBooking.appointment_time,
          visitor_name: finalBooking.visitor_name,
          email: finalBooking.email,
          phone: finalBooking.phone,
          appointment_date: finalBooking.appointment_date
        };
        // Clean response (remove JSON from user-facing text)
        const cleanResponse = this.cleanResponseFromJSON(geminiResponse);
        return {
          response: cleanResponse,
          updatedState,
          needsConfirmation: false,
          finalBooking
        };
      }
      
      // For regular conversation, let Gemini handle everything
      return {
        response: geminiResponse,
        updatedState: state, // Don't modify state during conversation
        needsConfirmation: false
      };
      
    } catch (error) {
      console.error('❌ Error processing conversation:', error);
      return {
        response: "I apologize, but I encountered an error. Please try again.",
        updatedState: state,
        needsConfirmation: false
      };
    }
  }

  private static async buildGeminiConversation(messages: ChatMessage[], state: AppointmentState): Promise<any[]> {
    // Fetch employees from API
    let employeeList = '';
    try {
      const employees = await apiService.getPublicEmployees();
      employeeList = employees.map(emp => `${emp.name} (${emp.department})`).join(', ');
      console.log('👥 Fetched employees from API:', employees);
    } catch (error) {
      console.error('Error fetching employees:', error);
      employeeList = 'No employees available';
    }
    
    const now = new Date();
    const currentTimeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const currentDateStr = now.toISOString().split('T')[0];
    
    const systemPrompt = `You are an intelligent appointment booking assistant for Kanishka Software. Your role is to have natural conversations with visitors to book appointments.

AVAILABLE EMPLOYEES: ${employeeList}

CRITICAL INSTRUCTIONS:
1. Handle the ENTIRE conversation flow naturally - collect all information through conversation
2. Be conversational and flexible - users can provide information in any order or format
3. When users want to change something, ask clarifying questions naturally:
   - "I want to change something" → "Sure! What would you like to change?"
   - "Change the name" → "Got it! What's your correct name?"
   - "No" (after summary) → "No problem! What would you like to change?"
   - "That's wrong" → "I understand. What specifically would you like to update?"
4. NEVER use rigid field extraction - let conversation flow naturally
5. Validate appointment times are between 9:00 AM and 4:30 PM
   -If the user selects a time that is already in the past **(for today)**, politely inform them and ask for a valid future time.
   - If the appointment is for a future date, accept any time.
   - If it's for today, compare the requested time with the current time. Reject if earlier.
   - Always assume the current local time is ${currentTimeStr} on ${currentDateStr}.
6. NEVER use emojis in responses - keep text clean and professional

REQUIRED INFORMATION TO COLLECT:
- Employee name (from the available list)
- Reason for appointment
- Time (today only, between 9:00 AM - 4:30 PM)
- Visitor name
- Email address
- Phone number

CONVERSATION FLOW:
1. Help users find the right employee if needed
2. Collect missing information naturally through conversation
3. Allow users to make changes in any format they want
4. When ALL information is collected, provide a summary
5. If user confirms everything is correct, generate the final booking

FINAL BOOKING FORMAT:
When user confirms all details are correct, respond with:
"Perfect! Your appointment has been booked successfully!"

Then include this EXACT JSON format (hidden from user):
BOOKING_JSON_START
{
  "employee_name": "Employee Name",
  "department": "Department",
  "reason": "Reason",
  "appointment_time": "Time",
  "visitor_name": "Visitor Name", 
  "email": "email@example.com",
  "phone": "1234567890",
  "appointment_date": "${currentDateStr}"
}
BOOKING_JSON_END

IMPORTANT: Only generate the JSON when user explicitly confirms all details are correct!`;

    const conversation = [
      {
        role: 'user',
        parts: [{ text: systemPrompt }]
      }
    ];

    // Add conversation history
    messages.forEach(msg => {
      if (msg.role === 'user') {
        conversation.push({
          role: 'user',
          parts: [{ text: msg.content }]
        });
      } else {
        conversation.push({
          role: 'model',
          parts: [{ text: msg.content }]
        });
      }
    });

    // Log the complete conversation being sent to Gemini
    console.log('🤖 COMPLETE GEMINI CONVERSATION DATA:');
    console.log('📅 Current time:', currentTimeStr);
    console.log('📅 Current date:', currentDateStr);
    console.log('👥 Employee list:', employeeList);
    console.log('💬 Conversation messages:', messages);
    console.log('🔄 Full conversation array:', JSON.stringify(conversation, null, 2));
    console.log('📋 System prompt length:', systemPrompt.length, 'characters');
    console.log('📋 Total conversation length:', JSON.stringify(conversation).length, 'characters');

    return conversation;
  }

  private static async callGeminiAPI(messages: any[]): Promise<string> {
    const requestBody = {
      contents: messages,
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 1024,
      },
    };

    console.log('🌐 GEMINI API REQUEST:');
    console.log('🔗 URL:', `${this.API_URL}?key=${this.API_KEY.substring(0, 10)}...`);
    console.log('📤 Request body:', JSON.stringify(requestBody, null, 2));
    console.log('📊 Request size:', JSON.stringify(requestBody).length, 'characters');

    const response = await fetch(`${this.API_URL}?key=${this.API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    console.log('📡 Gemini API response status:', response.status);
    console.log('📡 Gemini API response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Gemini API error response:', errorText);
      throw new Error(`Gemini API error: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('📥 Gemini API response data:', JSON.stringify(data, null, 2));
    
    const responseText = data.candidates[0]?.content?.parts[0]?.text || "I'm sorry, I couldn't process that. Please try again.";
    console.log('📝 Gemini response text:', responseText);
    
    return responseText;
  }

  private static extractFinalBookingJSON(response: string): AppointmentBooking | null {
    try {
      console.log('🔍 Looking for booking JSON in response...');
      
      // Look for the JSON between our markers
      const jsonMatch = response.match(/BOOKING_JSON_START\s*([\s\S]*?)\s*BOOKING_JSON_END/);
      if (!jsonMatch) {
        console.log('❌ No booking JSON markers found');
        return null;
      }
      
      const jsonString = jsonMatch[1].trim();
      console.log('📋 Found JSON string:', jsonString);
      
      const bookingData = JSON.parse(jsonString);
      
      // Validate required fields
      const requiredFields = ['employee_name', 'department', 'reason', 'appointment_time', 'visitor_name', 'email', 'phone'];
      const missingFields = requiredFields.filter(field => !bookingData[field]);
      
      if (missingFields.length > 0) {
        console.log('❌ Missing required fields:', missingFields);
        return null;
      }
      
      // Add appointment_date if not present
      if (!bookingData.appointment_date) {
        bookingData.appointment_date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD format
      }
      
      console.log('✅ Valid booking JSON extracted');
      return bookingData as AppointmentBooking;
      
    } catch (error) {
      console.error('❌ Error parsing booking JSON:', error);
      return null;
    }
  }

  private static cleanResponseFromJSON(response: string): string {
    // Remove the JSON section from the user-facing response
    return response.replace(/BOOKING_JSON_START[\s\S]*?BOOKING_JSON_END/g, '').trim();
  }

  // Helper method to find employee by name (for validation)
  private static async findEmployeeByName(name: string): Promise<{ name: string; department: string } | null> {
    try {
      const employees = await apiService.getPublicEmployees();
      const lowerName = name.toLowerCase();
      const employee = employees.find(emp => 
        emp.name.toLowerCase() === lowerName ||
        emp.name.toLowerCase().includes(lowerName) ||
        lowerName.includes(emp.name.toLowerCase())
      );
      return employee ? { name: employee.name, department: employee.department } : null;
    } catch (error) {
      console.error('Error finding employee by name:', error);
      return null;
    }
  }
}