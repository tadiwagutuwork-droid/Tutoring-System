# Tutoring-System

A modular Python-based tutoring management system designed to manage tutoring inquiries, students, tutors, users, queues, and persistent database storage.

The project was developed as a command-line application with a focus on **Object-Oriented Programming, modular design, database management, queue-based inquiry handling, error handling, and persistent storage**.

The system provides the foundation for a larger tutoring platform where students can submit tutoring requests and tutors can manage and claim those requests.

---

# Overview

The Tutoring Management System is designed to simplify the management of tutoring requests.

Instead of handling tutoring requests manually, the system allows inquiries to be submitted, stored, prioritised, and processed by tutors.

The application is structured into separate modules so that each part of the system has a specific responsibility.

The main components include:

- User and account management
- Student management
- Tutor management
- Tutoring inquiries
- Priority queues
- SQLite database management
- Persistent storage
- Command-line interaction
- Custom error handling
- Testing

The modular architecture allows the system to be expanded into a web-based tutoring platform in the future.

---

# Features

## User Management

The system supports different types of users and provides a foundation for managing user accounts.

Users can be represented by different roles, such as:

- Students
- Tutors
- Administrators

This allows the system to provide different functionality depending on the type of user interacting with the application.

---

## Tutoring Inquiries

Students can submit tutoring inquiries containing information about their tutoring requirements.

An inquiry can contain information such as:

- Inquiry ID
- Reference code
- Learner name
- Grade
- Subject
- Description
- Urgency
- Submission time
- Status
- Tutor assigned to the inquiry

---

## Priority Queue

Tutoring inquiries are managed using a queue system.

The queue allows inquiries to be processed according to their priority rather than simply processing them in the order in which they were submitted.

This is useful when some tutoring requests require more immediate attention than others.

---

## Database Storage

The system uses SQLite to store persistent information.

Database functionality is separated from the rest of the application through the `database` module.

This makes it easier to modify the database implementation without changing the rest of the system.

---

## Persistent Storage

The project contains a dedicated `storage` module for handling persistent data.

Earlier versions of the system used JSON-based storage, while later versions introduced SQLite database storage.

This development allowed the system to move from simple file-based persistence toward a more structured database architecture.

---

## Command-Line Interface

The current application provides a command-line interface.

The CLI allows users to interact with the tutoring system without directly interacting with the underlying classes or database.

The CLI is separated into its own module so that it does not become tightly coupled to the rest of the application.

---

## Custom Error Handling

The project contains a dedicated `errors` module for handling application-specific errors.

Custom errors allow the system to distinguish between different types of invalid operations and provide more meaningful feedback.

---

# System Workflow

A typical tutoring inquiry follows this process:

```text
                ┌──────────────────┐
                │     Student      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Submit Inquiry   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Store Inquiry    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Priority Queue   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Tutor Views      │
                │ Available Jobs   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Tutor Claims     │
                │ Inquiry          │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Inquiry Updated  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Tutoring Request │
                │ Processed        │
                └──────────────────┘

```

## Author

Tadiwa Gutu
