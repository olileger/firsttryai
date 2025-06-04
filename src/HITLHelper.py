import os
import sys
import datetime
import tempfile
import subprocess
from typing import Optional, Dict, Any, AsyncGenerator
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage


class HITLConsole:
    """
    A Human-in-the-Loop wrapper for the Console interface that allows users
    to review, approve, edit, or reject AI-generated actions before execution.
    """
    
    def __init__(self, response_stream: AsyncGenerator, enable_logging: bool = True):
        self._response_stream = response_stream
        self._enable_logging = enable_logging
        self._log_file = self._setup_logging() if enable_logging else None
        self._intervention_count = 0
    
    def _setup_logging(self) -> Optional[str]:
        """Setup logging for HITL interactions."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.expanduser("~/.ftry/hitl_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"hitl_session_{timestamp}.log")
        
        with open(log_file, 'w') as f:
            f.write(f"HITL Session Started: {datetime.datetime.now().isoformat()}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"🔄 HITL logging enabled. Session log: {log_file}")
        return log_file
    
    def _log_interaction(self, action: str, content: str, decision: str, edited_content: str = None):
        """Log HITL interactions for audit purposes."""
        if not self._enable_logging or not self._log_file:
            return
        
        timestamp = datetime.datetime.now().isoformat()
        self._intervention_count += 1
        
        with open(self._log_file, 'a') as f:
            f.write(f"[{timestamp}] Intervention #{self._intervention_count}\n")
            f.write(f"Action: {action}\n")
            f.write(f"Original Content:\n{content}\n")
            f.write(f"User Decision: {decision}\n")
            if edited_content and edited_content != content:
                f.write(f"Edited Content:\n{edited_content}\n")
            f.write("-" * 30 + "\n\n")
    
    def _present_action_for_review(self, content: str, message_type: str = "MESSAGE") -> tuple[str, str]:
        """
        Present an AI action to the user for review.
        Returns: (decision, potentially_edited_content)
        """
        print("\n" + "=" * 60)
        print(f"🤖 AI {message_type} REVIEW (Human-in-the-Loop)")
        print("=" * 60)
        print("The AI wants to send the following message:\n")
        print(content)
        print("\n" + "-" * 60)
        
        while True:
            print("What would you like to do?")
            print("  [a] Approve - Send the message as-is")
            print("  [e] Edit - Modify the message before sending")
            print("  [r] Reject - Cancel this message")
            print("  [v] View - Show the message again")
            
            choice = input("\nYour choice [a/e/r/v]: ").lower().strip()
            
            if choice == 'a':
                return 'approved', content
            elif choice == 'e':
                return self._edit_action(content)
            elif choice == 'r':
                print("❌ Message rejected by user")
                return 'rejected', None
            elif choice == 'v':
                print(f"\nOriginal {message_type.lower()}:")
                print(content)
                continue
            else:
                print("Invalid choice. Please enter 'a', 'e', 'r', or 'v'.")
    
    def _edit_action(self, content: str) -> tuple[str, str]:
        """Allow user to edit the action content."""
        print("\nChoose editing method:")
        print("  [i] Inline - Edit directly in terminal")
        print("  [e] External - Use $EDITOR (if available)")
        
        edit_choice = input("Editing method [i/e]: ").lower().strip()
        
        if edit_choice == 'e' and os.environ.get('EDITOR'):
            return self._edit_with_external_editor(content)
        else:
            return self._edit_inline(content)
    
    def _edit_with_external_editor(self, content: str) -> tuple[str, str]:
        """Edit content using external editor."""
        editor = os.environ.get('EDITOR', 'nano')
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            subprocess.run([editor, temp_file], check=True)
            
            with open(temp_file, 'r') as f:
                edited_content = f.read().strip()
            
            if edited_content != content:
                print("✏️  Content has been modified")
                return 'edited', edited_content
            else:
                print("No changes made")
                return 'approved', content
        
        except subprocess.CalledProcessError:
            print(f"Error opening editor {editor}. Falling back to inline editing.")
            return self._edit_inline(content)
        finally:
            os.unlink(temp_file)
    
    def _edit_inline(self, content: str) -> tuple[str, str]:
        """Edit content inline in the terminal."""
        print("\n📝 Inline Editing Mode")
        print("Enter your modified version (press Ctrl+D or empty line to finish):")
        print("\nCurrent content:")
        print(f"'{content}'")
        print("\nEnter modified content:")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
                # If user enters empty line and we already have content, stop
                if not line.strip() and lines:
                    break
        except EOFError:
            pass
        
        # Join all lines except the last empty one (if any)
        if lines and not lines[-1].strip():
            lines = lines[:-1]
        
        edited_content = '\n'.join(lines).strip()
        
        if edited_content and edited_content != content:
            print("✏️  Content has been modified")
            return 'edited', edited_content
        elif not edited_content:
            print("No changes made - approving original")
            return 'approved', content
        else:
            print("No changes made - approving original")
            return 'approved', content
    
    async def wrapped_stream(self):
        """Process the response stream with HITL intervention."""
        print("\n🔄 Starting Human-in-the-Loop session...")
        
        async for event in self._response_stream:
            # Intercept chat messages from AI agents
            should_review = False
            content_to_review = ""
            message_type = "EVENT"
            
            if isinstance(event, BaseChatMessage):
                # This is a chat message - review its content
                if hasattr(event, 'content') and event.content and event.content.strip():
                    should_review = True
                    content_to_review = str(event.content)
                    message_type = "MESSAGE"
            elif hasattr(event, '__dict__'):
                # Check if this is an agent event with content we should review
                event_dict = event.__dict__
                if 'content' in event_dict and event_dict['content'] and str(event_dict['content']).strip():
                    should_review = True
                    content_to_review = str(event_dict['content'])
                    message_type = "EVENT"
            
            if should_review:
                # Present action for review
                decision, modified_content = self._present_action_for_review(content_to_review, message_type)
                
                # Log the interaction
                self._log_interaction(f"AI_{message_type}", content_to_review, decision, modified_content)
                
                if decision == 'rejected':
                    print("🚫 Message rejected - skipping this event")
                    continue  # Skip this event
                elif decision == 'edited' and modified_content:
                    # Modify the event content
                    if isinstance(event, BaseChatMessage):
                        event.content = modified_content
                    elif hasattr(event, 'content'):
                        event.content = modified_content
                    print("✅ Message edited and approved - proceeding")
                else:
                    print("✅ Message approved - proceeding")
            
            # Yield the (potentially modified) event
            yield event
        
        if self._enable_logging and self._intervention_count > 0:
            print(f"\n📊 HITL Session Summary:")
            print(f"   Total interventions: {self._intervention_count}")
            print(f"   Session log: {self._log_file}")


async def create_hitl_console(response_stream: AsyncGenerator, enable_logging: bool = True):
    """
    Create a Human-in-the-Loop console wrapper.
    
    Args:
        response_stream: The original response stream
        enable_logging: Whether to enable logging of interactions
    
    Returns:
        Console with HITL wrapper
    """
    hitl_console = HITLConsole(response_stream, enable_logging)
    return await Console(hitl_console.wrapped_stream())