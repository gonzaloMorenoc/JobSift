"""Initial migration

Revision ID: 001_initial_migration
Revises: 
Create Date: 2024-11-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('locale', sa.String(length=5), nullable=True, default='en'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create interviews table
    op.create_table('interviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(length=100), nullable=False),
        sa.Column('company_description', sa.Text(), nullable=True),
        sa.Column('role_title', sa.String(length=100), nullable=False),
        sa.Column('work_mode', sa.Enum('REMOTE', 'HYBRID', 'ONSITE', name='workmode'), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('application_status', sa.Enum('APPLIED', 'SCREENING', 'HR_INTERVIEW', 'TECH_INTERVIEW', 'MANAGER_INTERVIEW', 'OFFER', 'REJECTED', 'ON_HOLD', name='applicationstatus'), nullable=True, default='APPLIED'),
        sa.Column('next_milestone', sa.String(length=200), nullable=True),
        sa.Column('contact_name', sa.String(length=100), nullable=True),
        sa.Column('contact_email', sa.String(length=100), nullable=True),
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('salary_range_min', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('salary_range_max', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True, default='USD'),
        sa.Column('language', sa.String(length=5), nullable=True, default='en'),
        sa.Column('travel_requirements', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('interview_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create calendar_events table
    op.create_table('calendar_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('external_event_id', sa.String(length=255), nullable=True),
        sa.Column('calendar_provider', sa.String(length=50), nullable=False),
        sa.Column('event_title', sa.String(length=200), nullable=False),
        sa.Column('event_description', sa.Text(), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_synced', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Add indexes for better performance
    op.create_index('ix_interviews_user_id', 'interviews', ['user_id'])
    op.create_index('ix_interviews_created_at', 'interviews', ['created_at'])
    op.create_index('ix_interviews_status', 'interviews', ['application_status'])
    op.create_index('ix_interviews_company', 'interviews', ['company_name'])
    op.create_index('ix_calendar_events_interview_id', 'calendar_events', ['interview_id'])

def downgrade():
    # Drop indexes
    op.drop_index('ix_calendar_events_interview_id')
    op.drop_index('ix_interviews_company')
    op.drop_index('ix_interviews_status')
    op.drop_index('ix_interviews_created_at')
    op.drop_index('ix_interviews_user_id')
    
    # Drop tables
    op.drop_table('calendar_events')
    op.drop_table('interviews')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS applicationstatus')
    op.execute('DROP TYPE IF EXISTS workmode')
    
    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
