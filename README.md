# ConasConnect

# Study System Authentication and Authorization Guide

## Overview
This document outlines how to implement authentication and authorization functionalities for ConasConnect in Django, accommodating three user roles: President, Publicity staff, and Students.

## User Roles and Models
- **Custom User Model**: Extend Django’s built-in `User` model to include fields like `mubis_special_no` for Mubis students.
- **User Roles**: Use Django’s `Group` and `Permission` system to manage roles:
  - **President**: Has permissions to upload and delete content.
  - **Publicity Secretary**: Also has permissions to upload and delete content.
  - **Students**: Divided into Mubis and non-Mubis categories.

## User Registration and Login
- **Registration**:
  - **Mubis Students**: Register with name, email, and `mubis_special_no`.
  - **Non-Mubis Students**: Register with name and email only.
- **Login**: Use Django’s authentication system. President and Publicity Secretary will log in directly without registration.

## Role-Based Access Control
- **Permissions**: Assign permissions using Django’s `Permission` system:
  - President and Publicity Secretary: Can upload and delete content.
  - Mubis Students: Access exclusive content (paid features).
  - Non-Mubis Students: See payment options for exclusive features.
- **Middleware**: Implement middleware to redirect users to appropriate interfaces based on their role.

## User Interface Customization
- **Templates**: Create separate templates for different roles:
  - **Mubis Students**: Access exclusive content.
  - **Non-Mubis Students**: See payment options.
  - **President and Publicity Secretary**: Content management interface.
- **Dynamic Content**: Use Django’s template tags to display content based on user roles.

## Payment Integration
- **Payment Options**: Integrate a payment gateway (e.g., Stripe, PayPal) for non-Mubis students.
- **Role Updates**: After payment, update the user’s role to grant access to exclusive content.

## Content Management
- **Upload and Delete**: Allow President and Publicity Secretary to manage content via Django’s admin or custom views.
- **Authorization Checks**: Use Django’s `@permission_required` decorator to restrict access.

## Implementation Steps
1. **Define User Roles and Models**:
   - Create a custom user model with necessary fields.
   - Set up groups and permissions for each role.

2. **User Registration and Login**:
   - Implement registration forms for Mubis and non-Mubis students.
   - Use Django’s authentication system for login.

3. **Role-Based Access Control**:
   - Assign permissions to groups.
   - Implement middleware for role-based redirection.

4. **User Interface Customization**:
   - Create templates for each role.
   - Use template tags for dynamic content display.

5. **Payment Integration**:
   - Set up payment gateway integration.
   - Update user roles after successful payments.

6. **Content Management**:
   - Allow authorized users to upload and delete content.
   - Use decorators to enforce permissions.

## Example Workflow
- **Mubis Student**: Registers with special number, gains access to exclusive content.
- **Non-Mubis Student**: Registers with basic info, sees payment options, upgrades after payment.
- **President/Publicity Secretary**: Logs in, manages content.

## Notes
- Use Django’s built-in tools for authentication and permissions.
- Customize templates and middleware to fit specific needs.
- Ensure secure handling of payment information.

This guide provides a structured understanding of our authentication system.
