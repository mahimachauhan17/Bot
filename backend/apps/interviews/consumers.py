import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Interview, InterviewMessage
import uuid

class InterviewConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time interview sessions
    Handles bidirectional communication between AI interviewer and candidate
    """
    
    async def connect(self):
        self.interview_id = self.scope['url_route']['kwargs']['interview_id']
        self.room_group_name = f'interview_{self.interview_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'interview_id': self.interview_id,
            'message': 'Connected to interview session'
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket
        """
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'candidate_message':
            await self.handle_candidate_message(data)
        elif message_type == 'start_interview':
            await self.handle_start_interview(data)
        elif message_type == 'end_interview':
            await self.handle_end_interview(data)
        elif message_type == 'audio_data':
            await self.handle_audio_data(data)
        elif message_type == 'video_frame':
            await self.handle_video_frame(data)
        elif message_type == 'connection_status':
            await self.handle_connection_status(data)
    
    async def handle_candidate_message(self, data):
        """
        Handle text message from candidate
        """
        content = data.get('content', '')
        
        # Save message to database
        message = await self.save_message(
            sender='candidate',
            message_type='answer',
            content=content
        )
        
        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'interview_message',
                'sender': 'candidate',
                'content': content,
                'message_id': str(message._id),
                'timestamp': message.timestamp.isoformat()
            }
        )
        
        # Generate AI response (this would call the AI service)
        # TODO: Integrate with AIService for intelligent follow-up
        ai_response = await self.generate_ai_response(content)
        
        # Save AI message
        ai_message = await self.save_message(
            sender='ai',
            message_type='followup',
            content=ai_response
        )
        
        # Send AI response
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'interview_message',
                'sender': 'ai',
                'content': ai_response,
                'message_id': str(ai_message._id),
                'timestamp': ai_message.timestamp.isoformat()
            }
        )
    
    async def handle_start_interview(self, data):
        """
        Handle interview start event
        """
        await self.update_interview_status('in_progress')
        
        # Send welcome message from AI
        welcome_message = "Hello! I'm your AI interviewer today. Let's begin the interview. Are you ready?"
        
        message = await self.save_message(
            sender='ai',
            message_type='system',
            content=welcome_message
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'interview_started',
                'message': welcome_message,
                'timestamp': message.timestamp.isoformat()
            }
        )
    
    async def handle_end_interview(self, data):
        """
        Handle interview end event
        """
        await self.update_interview_status('completed')
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'interview_ended',
                'message': 'Interview session ended. Thank you for your time!'
            }
        )
    
    async def handle_audio_data(self, data):
        """
        Handle audio data from candidate (for STT processing)
        """
        audio_data = data.get('audio')
        
        # TODO: Send to Google Speech-to-Text API
        # transcribed_text = await self.transcribe_audio(audio_data)
        
        # For now, echo back
        await self.send(text_data=json.dumps({
            'type': 'audio_processed',
            'status': 'received',
            'message': 'Audio data received for processing'
        }))
    
    async def handle_video_frame(self, data):
        """
        Handle video frame for analysis (facial expression, body language)
        """
        # TODO: Send to OpenCV/MediaPipe for analysis
        pass
    
    async def handle_connection_status(self, data):
        """
        Handle connection quality updates
        """
        status = data.get('status')
        quality = data.get('quality')
        
        await self.log_connection_event(status, quality)
    
    # Message handlers (called when messages are sent to the group)
    async def interview_message(self, event):
        """
        Receive message from room group and send to WebSocket
        """
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'content': event['content'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp']
        }))
    
    async def interview_started(self, event):
        """
        Handle interview started event
        """
        await self.send(text_data=json.dumps({
            'type': 'interview_started',
            'message': event['message'],
            'timestamp': event['timestamp']
        }))
    
    async def interview_ended(self, event):
        """
        Handle interview ended event
        """
        await self.send(text_data=json.dumps({
            'type': 'interview_ended',
            'message': event['message']
        }))
    
    # Database operations
    @database_sync_to_async
    def save_message(self, sender, message_type, content, question_id=None):
        """
        Save message to database
        """
        interview = Interview.objects.get(_id=self.interview_id)
        message = InterviewMessage.objects.create(
            interview=interview,
            sender=sender,
            message_type=message_type,
            content=content,
            question_id=question_id
        )
        return message
    
    @database_sync_to_async
    def update_interview_status(self, status):
        """
        Update interview status
        """
        from django.utils import timezone
        interview = Interview.objects.get(_id=self.interview_id)
        interview.status = status
        
        if status == 'in_progress' and not interview.started_at:
            interview.started_at = timezone.now()
        elif status == 'completed' and not interview.ended_at:
            interview.ended_at = timezone.now()
        
        interview.save()
        return interview
    
    @database_sync_to_async
    def log_connection_event(self, status, quality):
        """
        Log connection quality event
        """
        interview = Interview.objects.get(_id=self.interview_id)
        if not interview.connection_log:
            interview.connection_log = []
        
        from django.utils import timezone
        interview.connection_log.append({
            'timestamp': timezone.now().isoformat(),
            'status': status,
            'quality': quality
        })
        interview.save()
    
    async def generate_ai_response(self, candidate_message):
        """
        Generate AI response using LLM
        TODO: Integrate with OpenAI API
        """
        # Placeholder response
        return "That's an interesting point. Can you elaborate more on your experience with that?"
