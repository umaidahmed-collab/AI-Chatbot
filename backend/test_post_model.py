#!/usr/bin/env python
"""Test script to verify Post model is properly configured."""

import sys
sys.path.insert(0, '.')

from app.models.database import Post, User, Base

print("✓ Post model imported successfully")
print(f"✓ Post table name: {Post.__tablename__}")
print(f"✓ Post columns: {[c.name for c in Post.__table__.columns]}")
print(f"✓ User has posts relationship: {hasattr(User, 'posts')}")

# Verify all columns are present
required_columns = ['id', 'title', 'content', 'image_url', 'author_id', 'created_at', 'updated_at']
actual_columns = [c.name for c in Post.__table__.columns]

for col in required_columns:
    if col in actual_columns:
        print(f"✓ Column '{col}' exists")
    else:
        print(f"✗ Column '{col}' is missing!")
        sys.exit(1)

# Verify foreign key
fk_found = False
for col in Post.__table__.columns:
    if col.name == 'author_id' and col.foreign_keys:
        fk_found = True
        for fk in col.foreign_keys:
            print(f"✓ Foreign key: {col.name} -> {fk.target_fullname}")

if not fk_found:
    print("✗ Foreign key constraint is missing!")
    sys.exit(1)

print("\n✓ All Post model validations passed!")
