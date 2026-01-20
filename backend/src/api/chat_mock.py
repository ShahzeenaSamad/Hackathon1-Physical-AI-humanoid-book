"""
Mock Chat API - Demo version with hardcoded responses
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None
    top_k: int = 3

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[Dict]
    context_used: bool
    model_used: str

# Mock knowledge base
MOCK_RESPONSES = {
    "ros 2": {
        "answer": "ROS 2 (Robot Operating System 2) is an open-source middleware framework for building robot applications. It provides tools and libraries for hardware abstraction, device drivers, communication between processes, and package management. ROS 2 uses a Data Distribution Service (DDS) for communication, enabling real-time, reliable messaging between nodes. Key concepts include nodes (processes), topics (message streams), services (request-response), and actions (long-running goals with feedback). ROS 2 Humble is the recommended LTS release for 2024-2025.",
        "sources": [
            {"title": "Chapter 2: Introduction to ROS 2", "chapter_id": "module-1-chapter-02", "module": "Module 1: ROS 2 Fundamentals", "score": 0.95},
            {"title": "Chapter 3: ROS 2 Nodes and Topics", "chapter_id": "module-1-chapter-03", "module": "Module 1: ROS 2 Fundamentals", "score": 0.82}
        ]
    },
    "physical ai": {
        "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots. Unlike traditional digital AI that processes data in virtual environments, Physical AI must handle real-world complexities such as sensor noise, actuator delays, and dynamic environments. Humanoid robotics is a key application area where robots are designed with human-like form factors to operate in human-centric environments. Key challenges include perception, manipulation, locomotion, and human-robot interaction.",
        "sources": [
            {"title": "Chapter 1: Introduction to Physical AI", "chapter_id": "module-1-chapter-01", "module": "Module 1: ROS 2 Fundamentals", "score": 0.98}
        ]
    },
    "nodes": {
        "answer": "In ROS 2, a node is an executable process that performs computation. Nodes communicate via topics using a publish-subscribe pattern. A publisher node sends messages to a topic, and subscriber nodes receive those messages. Topics are typed - each topic has a specific message type. Common message types include std_msgs (String, Int32, Float64), geometry_msgs (Pose, Twist, Transform), and sensor_msgs (Image, LaserScan, Imu). You can create custom message types using .msg files.",
        "sources": [
            {"title": "Chapter 3: ROS 2 Nodes and Topics", "chapter_id": "module-1-chapter-03", "module": "Module 1: ROS 2 Fundamentals", "score": 0.96}
        ]
    },
    "simulation": {
        "answer": "Robot simulation enables testing algorithms without physical hardware, reducing costs and risks. Gazebo is a popular open-source 3D robot simulator providing physics simulation, sensor simulation, and ROS integration. Unity offers photorealistic rendering useful for visual perception tasks. Isaac Sim provides GPU-accelerated physics and advanced sensor simulation. The key tradeoff is simulation fidelity versus performance - high-fidelity physics simulations are computationally expensive.",
        "sources": [
            {"title": "Chapter 9: Introduction to Simulation", "chapter_id": "module-2-chapter-09", "module": "Module 2: Gazebo & Unity Simulation", "score": 0.93}
        ]
    },
    "isaac": {
        "answer": "NVIDIA Isaac Sim is a robot simulation platform built on Omniverse, providing photorealistic rendering and GPU-accelerated physics. Isaac ROS includes optimized perception packages for VSLAM, depth estimation, and object detection, leveraging CUDA acceleration on NVIDIA GPUs. The Isaac platform is designed for AI-powered robots with tight integration with deep learning frameworks. System requirements include RTX GPUs (RTX 4070 Ti or better recommended), though cloud alternatives exist via AWS or Omniverse Cloud.",
        "sources": [
            {"title": "Chapter 14: Introduction to NVIDIA Isaac", "chapter_id": "module-3-chapter-14", "module": "Module 3: NVIDIA Isaac Platform", "score": 0.94}
        ]
    },
    "vla": {
        "answer": "Vision-Language-Action (VLA) models combine computer vision, natural language processing, and robotic control in a unified framework. These models enable robots to understand high-level instructions like 'clean the table' and translate them into low-level actions. Large Language Models (LLMs) like GPT-4 serve as cognitive planners, decomposing complex tasks into executable subtasks. Examples include Google's RT-2 and PaLM-E, which demonstrate impressive generalization to new tasks and environments.",
        "sources": [
            {"title": "Chapter 19: Introduction to Vision-Language-Action (VLA)", "chapter_id": "module-4-chapter-19", "module": "Module 4: Vision-Language-Action Models", "score": 0.97}
        ]
    }
}

def get_mock_response(question: str) -> Dict:
    """Get mock response based on keywords in question"""
    question_lower = question.lower()

    # Check for keywords
    for keyword, response in MOCK_RESPONSES.items():
        if keyword in question_lower:
            return response

    # Default response
    return {
        "answer": "I'm a demo chatbot for the Physical AI & Humanoid Robotics textbook. I can answer questions about ROS 2, Physical AI, simulation (Gazebo, Unity, Isaac Sim), and Vision-Language-Action models. Try asking me: 'What is ROS 2?' or 'Tell me about Physical AI'",
        "sources": []
    }

@router.post("/query", response_model=ChatResponse)
async def chat_query_mock(request: ChatRequest):
    """Mock chatbot with predefined responses for demo"""

    # Get response based on question
    response_data = get_mock_response(request.question)

    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())

    return ChatResponse(
        session_id=session_id,
        answer=response_data["answer"],
        sources=response_data["sources"],
        context_used=True,
        model_used="mock-demo-v1"
    )
