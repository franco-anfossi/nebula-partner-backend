"""Mejora BD

Revision ID: befdc537d537
Revises: f97a7830c899
Create Date: 2024-11-03 03:17:02.779132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'befdc537d537'
down_revision: Union[str, None] = 'f97a7830c899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Habilitar la extensión `uuid-ossp` si no existe
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # Crear una columna temporal `id_temp` de tipo UUID con valores generados automáticamente
    op.add_column('user_profiles', sa.Column('id_temp', sa.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False))

    # Asignar un nuevo UUID para cada fila en `id_temp`
    op.execute("UPDATE user_profiles SET id_temp = uuid_generate_v4()")

    # Eliminar la restricción de clave foránea en `accounts.user_profile_id`
    op.drop_constraint('accounts_user_profile_id_fkey', 'accounts', type_='foreignkey')

    # Crear una columna temporal `user_profile_id_temp` de tipo UUID en `accounts`
    op.add_column('accounts', sa.Column('user_profile_id_temp', sa.UUID(), nullable=True))

    # Copiar valores a la columna `user_profile_id_temp` convertidos explícitamente
    op.execute("""
        UPDATE accounts 
        SET user_profile_id_temp = user_profile_id::uuid
        WHERE user_profile_id IS NOT NULL
    """)

    # Eliminar la columna `user_profile_id` antigua
    op.drop_column('accounts', 'user_profile_id')

    # Renombrar `user_profile_id_temp` a `user_profile_id`
    op.alter_column('accounts', 'user_profile_id_temp', new_column_name='user_profile_id', existing_type=sa.UUID, nullable=False)

    # Crear la clave foránea de nuevo
    op.create_foreign_key(
        'accounts_user_profile_id_fkey',
        'accounts', 'user_profiles',
        ['user_profile_id'], ['id_temp']
    )

    # Eliminar la columna `id` original y renombrar `id_temp` a `id`
    op.drop_column('user_profiles', 'id')
    op.alter_column('user_profiles', 'id_temp', new_column_name='id')

    # Resto de los comandos de migración
    op.drop_index('ix_user_company_invitations_id', table_name='user_company_invitations')
    op.drop_table('user_company_invitations')
    op.drop_index('ix_roles_id', table_name='roles')
    op.drop_table('roles')
    op.drop_index('ix_account_roles_id', table_name='account_roles')
    op.drop_table('account_roles')
    op.drop_column('accounts', 'created_at')
    op.drop_constraint('user_profiles_auth_id_key', 'user_profiles', type_='unique')
    op.drop_column('user_profiles', 'created_at')
    op.drop_column('user_profiles', 'auth_id')
    op.drop_column('user_profiles', 'is_active')


def downgrade() -> None:
    # Revertir todos los cambios en `downgrade`
    op.add_column('user_profiles', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user_profiles', sa.Column('auth_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('user_profiles', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_profiles_auth_id_key', 'user_profiles', ['auth_id'])
    op.alter_column('user_profiles', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               existing_server_default=sa.text("nextval('user_profiles_id_seq'::regclass)"))
    op.add_column('accounts', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.alter_column('accounts', 'user_profile_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.create_table('account_roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name='account_roles_account_id_fkey'),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='account_roles_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='account_roles_pkey')
    )
    op.create_index('ix_account_roles_id', 'account_roles', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('roles_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_roles_id', 'roles', ['id'], unique=False)
    op.create_table('user_company_invitations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_profile_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('invited_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_accepted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='user_company_invitations_company_id_fkey'),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_company_invitations_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], name='user_company_invitations_user_profile_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_company_invitations_pkey')
    )
    op.create_index('ix_user_company_invitations_id', 'user_company_invitations', ['id'], unique=False)
